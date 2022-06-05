import React from 'react';
import styled from 'styled-components';
import Input from './input';
import Output from './output';
import Button from './button';

const Container = styled.div`
  width: 100%;
  height: fit-content;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const FormWrapper = styled.div`
  width: 100%;
  height: fit-content;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 48px;
`;

const ButtonWrapper = styled.div`
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
`;

const Form = () => {
  return (
    <Container>
      <FormWrapper>
        <Input />
        <Output />
      </FormWrapper>
      <ButtonWrapper>
        <Button />
      </ButtonWrapper>
    </Container>
  );
};

export default Form;
