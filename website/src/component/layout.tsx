import React, {ReactNode} from 'react';
import styled from 'styled-components';

const Container = styled.main`
  width: 100vw;
  height: 100vh;
  background-color: #FFFFFF;
`;

interface LayoutProps {
    children: ReactNode
}

const Layout = ({children}: LayoutProps) => {
    return (
        <Container>
            {children}
        </Container>
    )
}

export default Layout
