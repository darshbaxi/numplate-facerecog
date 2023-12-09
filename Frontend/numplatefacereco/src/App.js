import './App.css';
import Registration from './components/Registration';
import Home from './components/home';
import {
  BrowserRouter,
  Routes,
  Route,

} from "react-router-dom";
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <>
     <Navbar bg="dark"  variant="dark">
        <Container>
          <Nav className="me-auto">
            <Nav.Link href="/">Home</Nav.Link>
            <Nav.Link href="/registration">Registration</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
   <BrowserRouter>
      <Routes>
        <Route path="/registration" element={<Registration />}/>
          <Route path="/" element={<Home />} />
        
      </Routes>
    </BrowserRouter>
    </>
  );
}

export default App;
