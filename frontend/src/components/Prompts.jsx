import { useState } from "react";
import { deletePrompt } from "../api/api";

function Prompts({ prompts, collections, refresh }) {

  const [expandedId, setExpandedId] = useState(null);
  const [selectedPrompts, setSelectedPrompts] = useState([]);

  /* GET COLLECTION NAME */

  const getCollectionName = (id) => {

    const collection = collections.find(c => c.id === id);

    return collection ? collection.name : "None";

  };

  /* TOGGLE EXPAND */

  const toggleExpand = (id) => {

    if (expandedId === id) {
      setExpandedId(null);
    } else {
      setExpandedId(id);
    }

  };

  /* SELECT PROMPTS */

  const toggleSelect = (id) => {

    if (selectedPrompts.includes(id)) {

      setSelectedPrompts(
        selectedPrompts.filter(x => x !== id)
      );

    } else {

      setSelectedPrompts([...selectedPrompts, id]);

    }

  };

  /* DELETE SELECTED */

  const deleteSelected = async () => {

    for (let id of selectedPrompts) {
      await deletePrompt(id);
    }

    setSelectedPrompts([]);

    refresh();

  };

  return (

    <div className="prompts-container">

      {selectedPrompts.length > 0 && (

        <button
          className="delete-selected"
          onClick={deleteSelected}
        >
          Delete Selected
        </button>

      )}

      {prompts.map(p => (

        <div key={p.id} className="prompt-row">

          {/* HEADER */}

          <div className="prompt-header">

            <input
              type="checkbox"
              checked={selectedPrompts.includes(p.id)}
              onChange={() => toggleSelect(p.id)}
            />

            <span
              className="prompt-title"
              onClick={() => toggleExpand(p.id)}
            >
              {p.title}
            </span>

          </div>

          {/* DETAILS */}

          {expandedId === p.id && (

            <div className="prompt-details">

              <div className="prompt-field">
                <strong>Title:</strong> {p.title}
              </div>

              <div className="prompt-field">
                <strong>Content:</strong> {p.content}
              </div>

              {p.description && (

                <div className="prompt-field">
                  <strong>Description:</strong> {p.description}
                </div>

              )}

              <div className="prompt-field">
                <strong>Collection:</strong> {getCollectionName(p.collection_id)}
              </div>

            </div>

          )}

        </div>

      ))}

    </div>

  );
}

export default Prompts;