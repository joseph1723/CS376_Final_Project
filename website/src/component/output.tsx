import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  width: calc(50% - 48px);
  height: 600px;
  border: 1px solid #cccccc;
`;

const Output = () => {
  return <Container>output 나올 자리</Container>;
};

export default Output;
