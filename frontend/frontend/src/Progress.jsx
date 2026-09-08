import { useEffect, useState } from "react";
import { studybotApi } from "./services/api";

export default function Progress({ setPage }) {
  const [overview, setOverview] = useState(null);
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([studybotApi.progress(), studybotApi.topicProgress()])
      .then(([stats, topicList]) => {
        setOverview(stats);
        setTopics(topicList || []);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const accuracy = overview?.overall_accuracy ?? 0;
  const statusClass = accuracy >= 75 ? "strong" : accuracy >= 50 ? "steady" : "focus";
  const statusText = accuracy >= 75 ? "On track" : accuracy >= 50 ? "Steady" : "Building";

  return (
    <section className="progress-page">
      <small>YOUR LEARNING STORY</small>
      <h1>Progress with purpose</h1>
      <p>Small, consistent efforts are creating strong foundations.</p>

      {error && <p className="api-error">{error}</p>}

      <div className="two-col">
        <article className="card weekly">
          <div className="title">
            <h2>Overall accuracy</h2>
            <span className={`tag ${statusClass}`}>{statusText}</span>
          </div>
          <div className="large">
            {loading ? "…" : `${accuracy}%`}{" "}
            <span>
              overall accuracy
              <br />
              <small>Target: 80%</small>
            </span>
          </div>
          <div className="progress">
            <i style={{ width: `${Math.min(100, accuracy)}%` }} />
            <b style={{ left: "80%" }} />
          </div>
          <div className="bars">▂▄▃▅▄▆▇</div>
        </article>

        <article className="card habit">
          <small>PRACTICE STATS</small>
          <h2>{overview?.total_attempted ?? 0} attempted</h2>
          <p>
            {overview?.correct_answers ?? 0} correct · {overview?.wrong_answers ?? 0} incorrect
          </p>
          <div className="days">
            {overview?.tests_completed ?? 0} tests completed
            <br />
            {overview?.wrong_answers ?? 0} items for revision
            <br />
            ● Live sync active
          </div>
        </article>
      </div>

      <section className="performance">
        <div className="title">
          <div>
            <h2>Topic breakdown</h2>
            <p>Calculated directly from every completed answer in your question sessions.</p>
          </div>
          {setPage && (
            <button className="filter" onClick={() => setPage("practice")}>
              Practice +
            </button>
          )}
        </div>
        <div className="subjects">
          {topics.length > 0 ? (
            topics.map((topic) => (
              <article key={topic.topic_id}>
                <div>
                  <b>{topic.name}</b>
                  <small>{topic.total_attempted} questions attempted</small>
                </div>
                <strong>{topic.accuracy_percentage}%</strong>
                <p>
                  <i style={{ width: `${Math.min(100, topic.accuracy_percentage)}%` }} />
                </p>
              </article>
            ))
          ) : (
            <p>No tests submitted yet. Start a session to build your metrics.</p>
          )}
        </div>
      </section>
    </section>
  );
}

