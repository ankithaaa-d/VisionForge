// sample-app/src/App.jsx
import "./App.css";

const features = [
  { title: "Fast capture", text: "Jot down ideas in under a second, on any device." },
  { title: "Smart search", text: "Find any note instantly with full-text search." },
  { title: "Sync everywhere", text: "Your notes follow you from laptop to phone." },
];

export default function App() {
  return (
    <div className="page">
      <header className="header">
        <div className="logo">Acme Notes</div>
        <nav className="nav">
          <a href="#features">Features</a>
          <a href="#pricing">Pricing</a>
          <a href="#signup">Sign up</a>
        </nav>
      </header>

      <main>
        <section className="hero">
          <h1>Capture ideas before they disappear</h1>
          <p>
            Acme Notes is a simple, fast notebook that keeps everything
            organized so you can focus on thinking.
          </p>
          <button className="btn" id="cta-button">Get started free</button>
        </section>

        <section id="features" className="features">
          {features.map((f) => (
            <article className="card" key={f.title}>
              <h2>{f.title}</h2>
              <p>{f.text}</p>
            </article>
          ))}
        </section>

        <section id="signup" className="signup">
          <h2>Join today</h2>
          <form onSubmit={(e) => e.preventDefault()}>
            <input type="email" placeholder="you@example.com" aria-label="Email" />
            <button className="btn" type="submit">Subscribe</button>
          </form>
        </section>
      </main>

      <footer className="footer">© 2026 Acme Notes</footer>
    </div>
  );
}