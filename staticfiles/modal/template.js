// Select the close button and modal element
const modal = document.querySelector('#modal-{{ modal_type }}'); // Use the dynamic modal ID
const closeBtn = document.querySelector('#modal-close-btn');


// Add event listener to the close button
closeBtn.addEventListener('click', () => {
  modal.style.display = 'none'; // Hides the modal
});