import membersData from '../data/members.json';

export function Members() {
    const renderMemberCard = (member) => {
        return `
            <div class="member-card">
                <div class="member-image-container">
                    <img src="${member.image}" alt="${member.name}" class="member-image" />
                </div>
                <div class="member-info">
                    <span class="member-role">${member.role}</span>
                    <h3 class="member-name">${member.name}</h3>
                    <p class="member-bio">${member.bio}</p>
                </div>
            </div>
        `;
    };

    return `
    <section class="nys-members">
        <div class="members-header">
            <h2>Our Team</h2>
            <p class="members-subtitle">Empowering Youth Since Day One</p>
            <p class="members-description">
                Organized and led by high-school students, Noble Youth Society is a non-profit organization based in Metro Vancouver, Canada.
            </p>
        </div>
        <div class="members-list">
            ${membersData.map(renderMemberCard).join('')}
        </div>
    </section>
  `;
}
