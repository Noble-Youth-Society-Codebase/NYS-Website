import { Hero } from './Hero.js';
import { ContentSection } from './ContentSection.js';
import { Contact } from './Contact.js';

export function Home() {
    return `
    ${Hero()}
    ${ContentSection()}
    ${Contact()}
  `;
}
