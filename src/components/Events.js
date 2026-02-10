import eventsData from '../data/events.json';

export function Events() {
    const renderEventItem = (item) => {
        const hasImage = !!item.image;
        // Layout logic: 'image-left' means image (or green box) is on left, text on right.
        // However, if there is no image, the 'title box' acts as the visual anchor.
        // Based on design:
        // With Image: Image (Left/Right) - Content (Right/Left)
        // Without Image: Green Title Box (Left/Right) - Content (Right/Left)

        // We can use a common structure:
        // <div class="event-item ${item.layout}">
        //   <div class="event-visual">...image or title box...</div>
        //   <div class="event-content">...text or title box...</div>
        // </div>

        // Actually, looking at the design:
        // If it has an image: Image is the visual. Title is in the content side (in a green box).
        // If it has NO image: The Title IS the visual (Green box with text). Content is the description.

        const isImageLeft = item.layout === 'image-left' || item.layout === 'text-right';
        // Wait, let's simplify. 
        // Visual Side (Image or Green Title Box)
        // Content Side (Description + Buttons (and Title if visual was Image))

        let visualContent = '';
        let textContent = '';

        if (hasImage) {
            visualContent = `<img src="${item.image}" alt="${item.title}" class="event-image" />`;
            textContent = `
            <div class="event-title-box">
                <h3>${item.title}</h3>
            </div>
            <div class="event-description-wrapper">
                <p class="event-date-text">${item.description}</p>
                <div class="event-buttons">
                    ${item.hasPhotos ? '<button class="btn-green">See Photos</button>' : ''}
                    ${item.hasArticle ? '<button class="btn-green">See Article</button>' : ''}
                </div>
            </div>
        `;
        } else {
            // No image -> The Title Box is the 'visual' anchor
            visualContent = `
            <div class="event-title-box-large">
                <h3>${item.title}</h3>
            </div>
        `;
            textContent = `
            <div class="event-description-wrapper">
                <p>${item.description}</p>
                 <div class="event-buttons">
                    ${item.hasPhotos ? '<button class="btn-green">See Photos</button>' : ''}
                    ${item.hasArticle ? '<button class="btn-green">See Article</button>' : ''}
                </div>
            </div>
        `;
        }

        // Determine order based on layout preference
        // layout: 'text-left' (Text comes first/left, Visual comes second/right)
        // layout: 'text-right' (Visual comes first/left, Text comes second/right)
        // wait, 'image-left' implies visual on left.
        // let's stick to standard flex-direction or order classes.

        const layoutClass = item.layout === 'text-left' ? 'layout-text-left' : 'layout-visual-left';

        return `
      <div class="event-item ${layoutClass}">
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

    const renderYearSection = (yearData) => {
        return `
      <section class="events-year-section">
        <h2 class="year-header">${yearData.year}</h2>
        <div class="year-events-list">
          ${yearData.items.map(renderEventItem).join('')}
        </div>
      </section>
    `;
    };

    return `
    <div class="events-container">
      ${eventsData.map(renderYearSection).join('')}
    </div>
  `;
}
