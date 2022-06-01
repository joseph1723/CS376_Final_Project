import React from 'react';
import styled from 'styled-components';
import Input from './input';
import Output from './output';

const Container = styled.div`
  width: 100%;
  height: fit-content;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`;

const Form = () => {
  return (
    <Container>
      <Input />
      <Output />
    </Container>
  );
};

export default Form;
