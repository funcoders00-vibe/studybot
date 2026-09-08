import { useEffect, useState } from "react";
import { studybotApi } from "./services/api";

function Review({ setPage, testId, setReviewing, setTestId }) {
  const [reviews, setReviews] = useState([]);
  const [activeIdx, setActiveIdx] = useState(0);
  const [loading, setLoading] = useState(Boolean(testId));
  const [error, setError] = useState(!testId ? "No test ID provided." : "");

  useEffect(() => {
    if (!testId) return;
    let cancelled = false;
    studybotApi.review(testId)
      .then((data) => {
        if (!cancelled) setReviews(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [testId]);

  if (loading) {
    return (
      <section className="review">
        <article className="card">
          <p>Loading answer review…</p>
        </article>
      </section>
    );
  }

  if (error || reviews.length === 0) {
    return (
      <section className="review">
        <div className="back">
          ‹ <button onClick={() => setReviewing(false)}>Test results</button>
        </div>
        <article className="card">
          <p className="api-error">{error || "No review answers available for this test."}</p>
        </article>
      </section>
    );
  }

  const item = reviews[activeIdx];
  const selectedText = item.options[item.selected_option] || "Not answered";
  const correctText = item.options[item.correct_option];

  return (
    <section className="review">
      <div className="back">
        ‹ <button onClick={() => setReviewing(false)}>Test results</button>
      </div>
      <h1>Answer review</h1>
      <p>Use each explanation as a calm step forward.</p>
      <article className="card">
        <div className="meta">
          <b>QUESTION {activeIdx + 1} OF {reviews.length}</b>
          <small className={item.is_correct ? "strong" : "error"}>
            {item.is_correct ? "Correct" : "Incorrect"}
          </small>
        </div>
        <h2>{item.question}</h2>

        {item.is_correct ? (
          <div className="good">
            <b>Your answer · {item.selected_option} (Correct)</b>
            {selectedText}
          </div>
        ) : (
          <>
            <div className="bad">
              <b>Your answer · {item.selected_option || "—"}</b>
              {selectedText}
            </div>
            <div className="good">
              <b>Correct answer · {item.correct_option}</b>
              {correctText}
            </div>
          </>
        )}

        <div className="explain">
          <b>Why this matters</b>
          <p>{item.explanation}</p>
          {(item.source_book || item.source_chapter) && (
            <p style={{ marginTop: "0.4rem", fontSize: "0.68rem", color: "var(--muted)" }}>
              Source: {item.source_book}{item.source_chapter ? ` · ${item.source_chapter}` : ""}{item.source_page ? ` · p. ${item.source_page}` : ""}
            </p>
          )}
        </div>
      </article>

      <div className="footer">
        {reviews.length > 1 && (
          <>
            <button
              disabled={activeIdx === 0}
              onClick={() => setActiveIdx((i) => Math.max(0, i - 1))}
            >
              ‹ Previous
            </button>
            <button
              disabled={activeIdx >= reviews.length - 1}
              onClick={() => setActiveIdx((i) => Math.min(reviews.length - 1, i + 1))}
            >
              Next question ›
            </button>
          </>
        )}
        <button onClick={() => { setTestId?.(null); setPage("dashboard"); }}>Finish review</button>
        <button className="primary" onClick={() => setPage("revision")}>
          Revise mistakes →
        </button>
      </div>
    </section>
  );
}

export default function TestResult({ setPage, testId, setTestId, user }) {
  const [reviewing, setReviewing] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(Boolean(testId));
  const [error, setError] = useState(!testId ? "No test ID provided." : "");

  useEffect(() => {
    if (!testId) return;
    let cancelled = false;
    studybotApi.result(testId)
      .then((data) => {
        if (!cancelled) setResult(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [testId]);

  if (reviewing) {
    return (
      <Review
        setPage={setPage}
        testId={testId}
        setReviewing={setReviewing}
        setTestId={setTestId}
      />
    );
  }

  return (
    <section className="result">
      <article className="card">
        <i>✦</i>
        <small>SESSION COMPLETE</small>
        <h1>Strong work, {user?.name || "Student"}!</h1>
        <p>
          You showed up with intention. Every question is a step toward mastery.
        </p>

        {loading ? (
          <p style={{ margin: "2rem 0" }}>Loading session results…</p>
        ) : error ? (
          <p className="api-error" style={{ margin: "1.5rem 0" }}>{error}</p>
        ) : (
          <>
            <div className="score">
              <b>{result ? `${result.score_percentage}%` : "—"}</b>
              <small>Accuracy</small>
            </div>
            <div className="result-stats">
              <div>
                <b>{result?.correct_answers ?? 0}</b>
                <small>Correct</small>
              </div>
              <div>
                <b>{result?.wrong_answers ?? 0}</b>
                <small>Incorrect</small>
              </div>
              <div>
                <b>{result?.total_questions ?? 0}</b>
                <small>Questions</small>
              </div>
              <div>
                <b>{result ? `+${result.correct_answers * 2}` : "0"}</b>
                <small>Points earned</small>
              </div>
            </div>
          </>
        )}

        <div className="actions">
          <button
            className="primary"
            disabled={!result}
            onClick={() => setReviewing(true)}
          >
            Review answers
          </button>
          <button onClick={() => { setTestId?.(null); setPage("dashboard"); }}>
            Back to dashboard
          </button>
        </div>
      </article>
    </section>
  );
}

