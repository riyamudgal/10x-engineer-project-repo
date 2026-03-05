import { useEffect, useState } from "react";

import Collections from "./components/Collections";
import PromptForm from "./components/PromptForm";
import Prompts from "./components/Prompts";
import Stats from "./components/Stats";

import {
  fetchPrompts,
  fetchCollections
} from "./api/api";

import "./styles.css";

function App() {

  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);

  /* DATA LOADING */

  useEffect(() => {

    async function loadData() {

      try {

        const promptsRes = await fetchPrompts();
        const collectionsRes = await fetchCollections();

        setPrompts(promptsRes.data.prompts);
        setCollections(collectionsRes.data.collections);

      } catch (error) {

        console.error("Error loading data:", error);

      }

    }

    loadData();

  }, []);

  /* REFRESH FUNCTION */

  const refresh = async () => {

    const promptsRes = await fetchPrompts();
    const collectionsRes = await fetchCollections();

    setPrompts(promptsRes.data.prompts);
    setCollections(collectionsRes.data.collections);

  };

  return (

    <div className="container">

      <h1>PromptLab</h1>

      <Stats />

      <div className="layout">

        <Collections
          collections={collections}
          refresh={refresh}
        />

        <div className="main">

          <PromptForm
            collections={collections}
            refresh={refresh}
          />

          <h2 className="section-title">Prompts</h2>

          <Prompts
            prompts={prompts}
            collections={collections}
            refresh={refresh}
          />

        </div>

      </div>

    </div>
  );
}

export default App;