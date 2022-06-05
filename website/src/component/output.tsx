import React from 'react';
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
`;

interface Props {
  res: string;
}

const Output = ({ res }: Props) => {
  return (
    <Container>
      <Header>Detection Result</Header>
      <ResponseWrapper>{res || ''}</ResponseWrapper>
    </Container>
  );
};

export default Output;
