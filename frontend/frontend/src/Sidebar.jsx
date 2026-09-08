const navigation = [
  ["dashboard", "⌂", "Dashboard"],
  ["study_chat", "💬", "Study Chat"],
  ["practice", "✎", "Practice"],
  ["test", "◈", "Mock Test"],
  ["revision", "↻", "Revision"],
  ["progress", "▥", "Progress"],
];

export default function Sidebar({ page, setPage }) {
  return (
    <>
      <aside>
        <button className="brand" onClick={() => setPage("dashboard")}>
          <i>S</i>
          <span>
            <b>StudyBot</b>
            <small>Personal Study Space</small>
          </span>
        </button>
        <nav>
          {navigation.map(([id, icon, label]) => (
            <button
              key={id}
              className={page === id ? "active" : ""}
              onClick={() => setPage(id)}
            >
              <i>{icon}</i>
              {label}
            </button>
          ))}
        </nav>
        <div className="focus">
          ●{" "}
          <span>
            <b>Focus Mode On</b>
            <small>Tranquil sanctuary</small>
          </span>
        </div>
      </aside>
      <nav className="bottom">
        {navigation.map(([id, icon, label]) => (
          <button
            key={id}
            className={page === id ? "active" : ""}
            onClick={() => setPage(id)}
          >
            <i>{icon}</i>
            <small>{label === "Dashboard" ? "Home" : label}</small>
          </button>
        ))}
      </nav>
    </>
  );
}
