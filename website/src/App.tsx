import React from 'react';
import styled from 'styled-components';
import Layout from './template/layout';
import './index.css';
import Header from './template/header';
import Form from './component/form';
import Footer from './template/footer';

const Container = styled.div`
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
`;

const App = () => {
  return (
    <Container>
      <Header />
      <Layout>
        <Form />
      </Layout>
      <Footer />
    </Container>
  );
};

export default App;
