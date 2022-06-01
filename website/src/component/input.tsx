import React, { useState } from 'react';
import styled from 'styled-components';

const Container = styled.textarea`
  width: calc(50% - 48px);
  height: 600px;
  border: 1px solid #cccccc;
`;

interface Props {
  title: string;
}

const Input = () => {
  const [value, setValue] = useState<string>('');

  return <Container value={value} onChange={e => setValue(e.target.value)} />;
};

export default Input;
