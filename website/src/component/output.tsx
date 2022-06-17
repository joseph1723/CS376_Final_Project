import React from 'react';
import styled from 'styled-components';
import { IRes } from './form';

const Container = styled.div`
  width: calc(50% - 32px);
  height: 500px;
  border: 1px solid #cccccc;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
`;

const Header = styled.div`
  width: 100%;
  height: 72px;
  padding: 0 16px;
  border-bottom: 1px solid #cccccc;
  background-color: #34568b33;
  display: flex;
  flex-direction: column;
  justify-content: center;
  font-size: 16px;
  font-weight: bold;
`;

const ResponseWrapper = styled.div`
  width: 100%;
  height: calc(100% - 72px);
  padding: 32px 16px;
  font-size: 16px;
  display: flex;
  flex-direction: column;
  
  span {
    margin-bottom: 8px;

    &.title {
      font-size: 20px;
      font-weight: bold;
      margin-bottom: 12px;
    }
  }
  
  .result {
    flex-direction: row;
    
    span {
      margin-right: 2px;
      
      &.hate {
        font-weight: bold;
        color : #FF0000;
      }
    }
  }
`;

interface Props {
  res?: IRes;
  req: string;
}

const Output = ({ res, req }: Props) => {
  return (
    <Container>
      <Header>Detection Result</Header>
      <ResponseWrapper>
          {res?.result === 0 && <span className="title">Hate speech!</span>}
          {res?.result === 1 && <span className="title">Not a hate speech!</span>}
          <div className="result">
              {res?.req.split(' ').map(((token, idx) => {
                  if(token) {
                      if(res?.index.includes(idx)) {
                          return (
                              <span className="hate">{token}</span>
                          );
                      } else {
                          return (
                              <span>{token}</span>
                          );
                      }
                  }
              }))}
          </div>
      </ResponseWrapper>
    </Container>
  );
};

export default Output;
