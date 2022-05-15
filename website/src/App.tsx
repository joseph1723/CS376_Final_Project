import React from 'react';
import styled from 'styled-components';
import Layout from './component/layout';
import './index.css';
import Header from './component/header';

const Container = styled.div`
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
`;

const App = () => {
  return (
    <Container>
      <Header />
      <Layout>CS376</Layout>
    </Container>
  );
};

export default App;
