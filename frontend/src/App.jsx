import { useEffect, useState } from "react";
import Prompts from "./components/Prompts";
import PromptForm from "./components/PromptForm";
import Collections from "./components/Collections";
import Stats from "./components/Stats";
import { fetchPrompts, fetchCollections } from "./api/api";
import "./styles.css";

function App() {

  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);

  useEffect(() => {

    const loadData = async () => {

      try {
        const p = await fetchPrompts();
        const c = await fetchCollections();

        setPrompts(p.data.prompts);
        setCollections(c.data.collections);

      } catch (err) {
        console.error("Failed to load data", err);
      }

    };

    loadData();

  }, []);

  return (
    <div className="container">

      <h1>PromptLab</h1>

      <Stats />

      <div className="layout">

        <Collections
          collections={collections}
        />

        <div className="main">

          <PromptForm
            collections={collections}
          />

          <Prompts
            prompts={prompts}
            collections={collections}
          />

        </div>

      </div>

    </div>
  );
}

export default App;