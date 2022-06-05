import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  width: 100%;
  height: 90px;
  padding: 16px 32px;
  border-bottom: 1px solid #dae3f1;
  background-color: #34568b;
  color: #ffffff;
  display: flex;
  flex-direction: row;
  align-items: center;

  span {
    font-size: 20px;
    font-weight: bold;
  }
`;

const Header = () => {
  return (
    <Container>
      <span>CS376 Hate Speech Detection</span>
    </Container>
  );
};

export default Header;
