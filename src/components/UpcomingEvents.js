import upcomingEventsData from '../data/upcoming-events.json';

export function UpcomingEvents() {
    const renderEventItem = (item) => {
        // Theme handling: 'red' vs default 'green'
        const themeClass = item.theme === 'red' ? 'theme-red' : 'theme-green';
        const titleBoxClass = item.theme === 'red' ? 'event-title-box-red' : 'event-title-box';

        const hasImage = !!item.image;
        let visualContent = '';
        let textContent = '';

        if (hasImage) {
            visualContent = `<img src="${item.image}" alt="${item.title}" class="event-image" />`;
            textContent = `
                <div class="${titleBoxClass}">
                    <h3>${item.title}</h3>
                </div>
                <div class="event-description-wrapper">
                    <p class="event-date-text">${item.description}</p>
                </div>
            `;
        }

        // Upcoming events seem to generally have images based on the design (flyers)
        // If not, we can fallback to logic similar to Events.js

        return `
            <div class="event-item layout-visual-left ${themeClass}">
                <div class="event-visual-col">
                    ${visualContent}
                </div>
                <div class="event-text-col">
                    ${textContent}
                </div>
            </div>
            <div class="event-divider"></div>
        `;
    };

    return `
    <div class="events-container">
        <div class="upcoming-events-list">
            ${upcomingEventsData.map(renderEventItem).join('')}
        </div>
        
        <div class="coming-soon-section">
            <h2>(More) Coming Soon</h2>
            <h2>Stay Tuned</h2>
            <h2>: )</h2>
        </div>
    </div>
  `;
}
