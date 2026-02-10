export function Contact() {
    return `
    <section class="nys-contact" id="join">
      <div class="contact-wrapper">
        <div class="contact-header">
           <h2>CONTACT US</h2>
           <!-- Empty space or text if needed on left -->
        </div>
        <div class="contact-form-container">
          <form class="nys-form">
            <div class="form-row">
              <div class="form-group">
                <label for="name">Name</label>
                <input type="text" id="name" name="name" required>
              </div>
              <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
              </div>
            </div>
            <div class="form-row">
               <div class="form-group">
                <label for="phone">Phone</label>
                <input type="tel" id="phone" name="phone">
              </div>
              <div class="form-group">
                <label for="address">Address</label>
                <input type="text" id="address" name="address">
              </div>
            </div>
            <div class="form-group">
              <label for="subject">Subject</label>
              <input type="text" id="subject" name="subject">
            </div>
            <div class="form-group">
              <label for="message">Type your message here...</label>
              <textarea id="message" name="message" rows="4"></textarea>
            </div>
            <button type="submit" class="btn-submit">Submit</button>
          </form>
        </div>
      </div>
    </section>
  `;
}
