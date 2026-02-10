import './style.css';
import { Header } from './components/Header.js';
import { Home } from './components/Home.js';
import { Events } from './components/Events.js';
import { UpcomingEvents } from './components/UpcomingEvents.js';
import { Join } from './components/Join.js';
import { Members } from './components/Members.js';
import { Footer } from './components/Footer.js';

const render = () => {
  const app = document.querySelector('#app');
  const path = window.location.pathname;

  let component;

  if (path.includes('upcoming-events.html')) {
    component = UpcomingEvents;
  } else if (path.includes('events.html')) {
    component = Events;
  } else if (path.includes('join.html')) {
    component = Join;
  } else if (path.includes('members.html')) {
    component = Members;
  } else {
    component = Home;
  }

  app.innerHTML = `
    ${Header()}
    <main id="main-content">
      ${component()}
    </main>
    ${Footer()}
  `;
};

window.addEventListener('DOMContentLoaded', render);
// Render immediately
render();
