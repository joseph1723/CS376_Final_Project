import torch, string, re
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

VOCAB_SIZE = 128 + 2
EOS, SOS, PAD = 128, 129, 0

def ascii_range(text) :
    for c in text :
        if ord(c) not in range(128) : return False
    return True

def preprocess_words(texts, max_len, is_source=True) :
    #max_len = max([len(t) for t in texts])
    out = []
    for text in texts :
        encoded = [ord(c) for c in text] + [EOS] + [PAD] * (max_len - len(text))
        if not is_source :
            encoded = [SOS] + encoded
        out.append(torch.tensor(encoded))
    return out  #, max_len

def tensor_to_str(t) :
  #tensor t : (N,Max_len)
  N = t.shape[0]
  str_list = []
  for i in range(N) :
    row = t[i,:]
    decoded = "".join([chr(c) for c in row if c in range(1,128)])
    str_list.append(decoded)
  return str_list

def spellcheck(words, model, device, model_type="lstm") :
    #input : list of strings(words)

    #Get model
    model = model.to(device)

    #Preprocess input
    max_len = max([len(i) for i in words])
    src = preprocess_words(words, max_len)

    src_len = torch.tensor([t.shape[0] for t in src], dtype=torch.int64)
    src = torch.cat([torch.unsqueeze(s, dim=0) for s in src], dim=0).to(device)

    #Do the prediction & print
    if model_type=="lstm" :
        prediction = tensor_to_str(model.predict(src, src_len))
    elif model_type=="rnn" :
        prediction = tensor_to_str(model(src, src_len)[0])
    else :
        prediction = None
    return prediction

def spell_correction(text, tokenizer, vocab, model, device, model_type="lstm") :
    tokenized_words = tokenizer.tokenize(text)
    #new_words = []
    new_text = text
    re_punkt = re.compile("[" + string.punctuation + "]+")
    
    out_of_vocab_words = [word for word in tokenized_words if (word.lower() not in vocab) and not re_punkt.fullmatch(word)]
    #pred_words = [word.lower() for word in out_of_vocab_words]
    pred_words = spellcheck(out_of_vocab_words, model, device, model_type=model_type)

    for (word, new_word) in zip(out_of_vocab_words, pred_words) :
        new_text = text.replace(word, new_word)
        
    return new_text

def masked_softmax(X, valid_length):
  mask_value = -1e7 

  if len(X.shape) == 2:
    X = X.unsqueeze(1)

  N, n, m = X.shape

  if len(valid_length.shape) == 1:
    valid_length = valid_length.repeat_interleave(n, dim=0)
  else:
    valid_length = valid_length.reshape((-1,))

  mask = torch.arange(m)[None, :].to(X.device) >= valid_length[:, None]
  X.view(-1, m)[mask] = mask_value

  Y = torch.softmax(X, dim=-1)
  return Y

class DotProductAttention(nn.Module): 
  def __init__(self):
      super(DotProductAttention, self).__init__()

  def forward(self, query, key, value, valid_length=None):
    B, n, d = query.shape
    d_sqrt = torch.sqrt(query.new_tensor([d]))
    a = torch.div(torch.bmm(query, torch.transpose(key,1,2)), d_sqrt)

    b = masked_softmax(a, valid_length)
    #print(value.shape, value)
    #rint(b.shape, b)

    attention = torch.bmm(b, value)

    return attention

class Encoder(nn.Module):
  def __init__(self, vocab_size, embedding_dim, hidden_size, device):
    super(Encoder, self).__init__()
    self.embedding = nn.Embedding(vocab_size, embedding_dim)
    self.enc = nn.LSTM(embedding_dim, hidden_size, batch_first=True, bidirectional=False)  #input_size, hidden_size, num_layers, bias, batch_first(TRUE -> (B,MAX_LEN,emb_dim)), dropout, bi-directional
    self.hidden_size = hidden_size
    self.device = device
    
  def forward(self, sources, valid_len):
    #(B,Max_len)
    #print(sources)
    word_embedded = self.embedding(sources)
    packed_input = pack_padded_sequence(word_embedded, valid_len, batch_first=True, enforce_sorted=False)

    N = word_embedded.shape[0]  #(N, Max_len, emb_dim)
    max_len = word_embedded.shape[1]
    
    #(D*num_layers), N, H_out / D=2(bi-directional), num_layers=1, N=batch_size, H_out=hidden_size 
    h = sources.new_zeros(1, N, self.hidden_size).float()
    c = sources.new_zeros(1, N, self.hidden_size).float()

    #output_size : (N, L, D*H_out) when batch_first=True
    outputs, (h, c) = self.enc(packed_input, (h, c))
    packed_output, _ = pad_packed_sequence(outputs, padding_value= 0, batch_first=True, total_length=max_len)

    return packed_output, (h, c)

class Decoder(nn.Module):
  def __init__(self, vocab_size, embedding_dim, hidden_size, device):
    super(Decoder, self).__init__()
    self.embedding = nn.Embedding(vocab_size, embedding_dim)
    self.enc = nn.LSTM(embedding_dim+hidden_size, hidden_size, batch_first=True, bidirectional=False)
    self.output_emb = nn.Linear(hidden_size, vocab_size)
    self.att = DotProductAttention()
    self.embedding_dim = embedding_dim
    self.hidden_size = hidden_size
    self.device = device
    
  def forward(self, state, target, valid_len):
    device = self.device
    loss = 0
    preds = []
    enc_output, (h, c), src_len = state
    enc_output = enc_output.to(device)

    #print(target)
    target_embedded = self.embedding(target)
    N, max_len = target_embedded.shape[:2]  #T : MAX sequence-length

    dec_output = enc_output.new_zeros(N,max_len,self.hidden_size).to(device)
    for i in range(max_len) :
      context = self.att(h.transpose(0,1), enc_output, enc_output, valid_length=src_len.to(device))

      dec_input = torch.cat((target_embedded[:,i,:].reshape(N,1,-1), context), dim=2)
      dec_words, (h, c) = self.enc(dec_input, (h, c))    #dec_words : (N,1,hidden_size)
      dec_output[:,i,:] = dec_words.reshape(N,self.hidden_size)   #(N,T,hidden_size)

    preds = self.output_emb(dec_output)   #preds : (N,Max_len,vocab_size)

    loss = F.nll_loss(F.log_softmax(preds[:, :max_len-1].transpose(1,2), dim = 1), target[:, 1:], ignore_index=0, reduction = 'none')
    loss = loss.sum(1).mean()

    preds = preds.argmax(dim=-1)
    # END OF YOUR CODE
    return loss, preds
  
  def predict(self, state, target=None, valid_len=None):
    device = self.device
    pred = None
    enc_output, (h, c), src_len = state
    enc_output = enc_output.to(self.device)
    N, max_len = enc_output.shape[:2]  #T : MAX sequence-length

    preds = []
    pred_prev = self.embedding(torch.full((N,1,1),fill_value=SOS).to(self.device)).reshape(N,1,-1)

    for i in range(max_len) :
      context = self.att(h.transpose(0,1), enc_output, enc_output, valid_length=src_len.to(self.device))
      dec_input = torch.cat((pred_prev, context), dim=2)
      dec_words, (h, c) = self.enc(dec_input, (h, c))    #dec_words : (N,1,hidden_size)
      dec_words_output = self.output_emb(dec_words.to(self.device)).argmax(dim=-1)   #(hidden_size -> vocab_size)
      preds.append(dec_words_output)
      pred_prev = self.embedding(dec_words_output)    #(vocab_size -> emb_dim)
    
    pred = torch.cat(preds, dim=1).to(self.device)

    return pred

class NMTLSTM(nn.Module):
  def __init__(self, src_vocab_size, tgt_vocab_size, embedding_dim, hidden_size, device):
    super(NMTLSTM, self).__init__()
    self.enc = Encoder(src_vocab_size, embedding_dim, hidden_size, device)
    self.dec = Decoder(tgt_vocab_size, embedding_dim, hidden_size, device)
    
  def forward(self, src, src_len, tgt, tgt_len):
    outputs, (h, c) = self.enc(src, src_len)
    loss, pred = self.dec((outputs, (h, c), src_len), tgt, tgt_len)
    return loss, pred
  
  def predict(self, src, src_len, tgt=None, tgt_len=None):
    outputs, (h, c) = self.enc(src, src_len)
    pred = self.dec.predict((outputs, (h, c), src_len), tgt, tgt_len)
    return pred

class BaseRNN(nn.Module):
  def __init__(self, vocab_size, embedding_dim, hidden_size, device=None):
    super(BaseRNN, self).__init__()
    self.num_layers = 1
    self.embedding = nn.Embedding(vocab_size, embedding_dim)
    self.enc = nn.RNN(embedding_dim, hidden_size, num_layers=self.num_layers, batch_first=True, bidirectional=True)  #input_size, hidden_size, num_layers, bias, batch_first(TRUE -> (B,MAX_LEN,emb_dim)), dropout, bi-directional
    self.ln1 = nn.Linear(2*hidden_size, vocab_size)

    self.hidden_size = hidden_size
    self.embedding_dim = embedding_dim
    
  def forward(self, sources, valid_len):
    #(B,Max_len)
    word_embedded = self.embedding(sources)
    packed_input = pack_padded_sequence(word_embedded, valid_len, batch_first=True, enforce_sorted=False)

    N = word_embedded.shape[0]  #(N, Max_len, emb_dim)
    max_len = word_embedded.shape[1]
    
    #(D*num_layers), N, H_out / D=2(bi-directional), num_layers=1, N=batch_size, H_out=hidden_size 
    h = sources.new_zeros(2*self.num_layers, N, self.hidden_size).float()
    #c = sources.new_zeros(2*self.num_layers, N, self.hidden_size).float()

    #output_size : (N, L, D*H_out) when batch_first=True
    outputs, h = self.enc(packed_input, h)
    packed_output, _ = pad_packed_sequence(outputs, padding_value= 0, batch_first=True, total_length=max_len)

    #linear_output : (N, L, Vocab_size)
    lin_output = self.ln1(packed_output)

    #Final_Output : (N, L, 1)
    preds = lin_output.argmax(dim=-1)
    return preds, lin_output