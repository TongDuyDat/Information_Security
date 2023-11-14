import Login from "./Login";
import Key from "./key";
import Home from "./Home/home";
import Register from "./register";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dangky" element={<Register />} />
        <Route path="/home" element={<Home/>} />
        <Route path="/key" element={<Key/>}/>
      </Routes>
    </Router>
  );
}

export default App;
