import { Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import PromptsPage from "./pages/PromptsPage";
import CollectionsPage from "./pages/CollectionsPage";

function App() {

  return (
    <div>

      <Navbar />

      <Routes>

        <Route path="/" element={<Dashboard />} />

        <Route path="/prompts" element={<PromptsPage />} />

        <Route path="/collections" element={<CollectionsPage />} />

      </Routes>

    </div>
  );
}

export default App;