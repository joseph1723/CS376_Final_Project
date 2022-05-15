import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  width: 100%;
  height: 74px;
  padding: 0 32px;
  border-bottom: 1px solid #cccccc;
  background-color: #ffffff;
  display: flex;
  flex-direction: row;
  align-items: center;
`;

const Header = () => {
  return <Container>파파고</Container>;
};

export default Header;
