




document.addEventListener('DOMContentLoaded', function() {
  // Scroll to section if URL parameter is present
  const urlParams = new URLSearchParams(window.location.search);
  const scrollToSection = urlParams.get('scrollTo');

  if (scrollToSection) {
    const section = document.getElementById(scrollToSection);
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
  }

  // Add click event to the Our Team link to navigate to the dashboard
  const ourTeamLink = document.getElementById('our-team-link');
  ourTeamLink.addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = `${ourTeamLink.href}?scrollTo=client-section`;
  });
});
