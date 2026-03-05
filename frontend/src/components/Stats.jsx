import { useEffect, useState } from "react";
import { fetchStats } from "../api/api";

function Stats() {

  const [stats, setStats] = useState({});

  useEffect(() => {

    async function load() {
      const res = await fetchStats();
      setStats(res.data);
    }

    load();

  }, []);

  return (
    <div className="stats">

      <p>Total Prompts: {stats.total_prompts}</p>
      <p>Total Collections: {stats.total_collections}</p>
      <p>No Collection: {stats.prompts_without_collection}</p>

    </div>
  );
}

export default Stats;