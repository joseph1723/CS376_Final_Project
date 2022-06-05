import React from 'react';
import styled from 'styled-components';

const Wrapper = styled.div`
  width: 200px;
  height: 60px;
  border-radius: 8px;
  background-color: #98b4d4;
  padding: 8px 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  cursor: pointer;

  &:hover {
    box-shadow: 4px 4px 4px #cccccccc;
  }
`;

const Button = () => {
  return <Wrapper>Run Model</Wrapper>;
};

export default Button;
