export function Header() {
  return `
    <header class="nys-header">
      <div class="header-top">
        <div class="logo-wrapper">
            <img src="/assets/logo.png" alt="NYS Logo" class="nys-logo-img" />
        </div>
        <div class="title-wrapper">
            <span class="logo-text-large">NOBLE YOUTH SOCIETY</span>
        </div>
      </div>
      <div class="header-divider"></div>
      <nav class="nys-nav">
        <ul>
          <li><a href="/index.html">HOME</a></li>
          <li><a href="/events.html">PAST EVENTS</a></li>
          <li><a href="/upcoming-events.html">UPCOMING EVENTS</a></li>
          <li><a href="/members.html">OUR MEMBERS</a></li>
          <li><a href="/join.html">JOIN US</a></li>
        </ul>
      </nav>
    </header>
  `;
}
