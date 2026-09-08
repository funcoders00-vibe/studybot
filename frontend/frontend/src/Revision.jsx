import { useEffect, useState } from "react";
import { studybotApi } from "./services/api";

export default function Revision({ setPage, setTestId }) {
  const [wrongAnswers, setWrongAnswers] = useState([]);
  const [topics, setTopics] = useState([]);
  const [selectedTopicId, setSelectedTopicId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([studybotApi.wrongAnswers(), studybotApi.topics()])
      .then(([wrongList, topicList]) => {
        setWrongAnswers(wrongList || []);
        setTopics(topicList || []);
        if (wrongList && wrongList.length > 0) {
          setSelectedTopicId(wrongList[0].topic_id);
        } else if (topicList && topicList.length > 0) {
          setSelectedTopicId(topicList[0].id);
        }
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const topicMap = new Map(topics.map((t) => [t.id, t.name]));
  const topicCounts = wrongAnswers.reduce((acc, item) => {
    acc[item.topic_id] = (acc[item.topic_id] || 0) + 1;
    return acc;
  }, {});

  const topicIdsWithMistakes = Object.keys(topicCounts).map(Number);
  const activeTopicId = selectedTopicId ?? (topicIdsWithMistakes[0] || topics[0]?.id);
  const activeTopicName = topicMap.get(activeTopicId) || "Selected Topic";
  const activeCount = topicCounts[activeTopicId] || 0;

  async function startRevisionSession() {
    if (!activeTopicId) return;
    setStarting(true);
    setError("");
    try {
      const test = await studybotApi.startRevision({
        topic_id: Number(activeTopicId),
        number_of_questions: Math.min(activeCount || 1, 20),
      });
      setTestId(test.test_id);
      setPage("question");
    } catch (err) {
      setError(err.message || "Failed to start revision session.");
      setStarting(false);
    }
  }

  return (
    <section className="revision">
      <div className="title">
        <div>
          <small>SPACED REPETITION</small>
          <h1>Your revision sanctuary</h1>
          <p>Gentle review today builds lasting recall tomorrow.</p>
        </div>
        <div className="ring">
          <b>{loading ? "…" : wrongAnswers.length}</b>
          <small>due today</small>
        </div>
      </div>

      {error && <p className="api-error">{error}</p>}

      <div className="two-col">
        <article className="card revision-main">
          {wrongAnswers.length > 0 ? (
            <>
              <span className="tag strong">Ready for review</span>
              <h2>{activeTopicName}</h2>
              <p>
                {activeCount} question{activeCount === 1 ? "" : "s"} ready for recall.
                A focused revision session takes about {Math.max(2, Math.round(activeCount * 1.5))} minutes.
              </p>

              {topicIdsWithMistakes.length > 1 && (
                <div style={{ margin: "1rem 0" }}>
                  <label style={{ fontSize: "0.72rem", color: "var(--muted)", fontWeight: "700" }}>
                    Select topic to revise:
                    <select
                      value={activeTopicId}
                      onChange={(e) => setSelectedTopicId(Number(e.target.value))}
                      style={{
                        display: "block",
                        width: "100%",
                        marginTop: "0.3rem",
                        padding: "0.5rem",
                        borderRadius: "0.5rem",
                        border: "1px solid var(--line)",
                      }}
                    >
                      {topicIdsWithMistakes.map((id) => (
                        <option key={id} value={id}>
                          {topicMap.get(id) || `Topic ${id}`} ({topicCounts[id]} cards)
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
              )}

              <div className="memory">━━━━━</div>
              <button
                className="primary"
                disabled={starting || activeCount === 0}
                onClick={startRevisionSession}
              >
                {starting ? "Preparing session…" : "Begin daily revision →"}
              </button>
            </>
          ) : (
            <>
              <span className="tag strong">All clear</span>
              <h2>No mistakes pending</h2>
              <p>You have reviewed all flagged questions! Take a practice session to continue learning.</p>
              <div className="memory">━━━━━</div>
              <button className="primary" onClick={() => setPage("practice")}>
                Start a practice test →
              </button>
            </>
          )}
        </article>

        <article className="card rhythm">
          <small>MEMORY RHYTHM</small>
          <h2>{wrongAnswers.length === 0 ? "Balanced and steady" : "Active recall"}</h2>
          <div>▁▃▂▅▄▆▇</div>
          <p>
            {wrongAnswers.length === 0
              ? "Your answered questions are verified. Keep momentum with continuous tests."
              : `${wrongAnswers.length} mistake${wrongAnswers.length === 1 ? "" : "s"} awaiting spaced recall.`}
          </p>
        </article>
      </div>
    </section>
  );
}

