import React, { useState } from 'react';
import styled from 'styled-components';

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
  font-size: 16px;
  font-weight: bold;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
`;

const TextArea = styled.textarea`
  width: 100%;
  height: calc(100% - 72px);
  border: none;
  border-radius: 0;
  outline: none;
  padding: 32px 16px;
  font-size: 16px;
`;

interface Props {
  setReq: (req: string) => void;
}

const Input = ({ setReq }: Props) => {
  const [value, setValue] = useState<string>('');

  return (
    <Container>
      <Header>Input String</Header>
      <TextArea
        value={value}
        onChange={e => {
          setValue(e.target.value);
          setReq(e.target.value);
        }}
        placeholder={'문장을 입력해주세요'}
      />
    </Container>
  );
};

export default Input;
