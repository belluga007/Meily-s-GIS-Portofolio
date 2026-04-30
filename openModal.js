function openModal(element) {
  const modal = document.getElementById("imageModal");
  const modalImg = document.getElementById("modalImg");
  const captionText = document.getElementById("caption");

  modal.style.display = "block";
  modalImg.src = element.src; // Uses the src from your <img> tag
  captionText.innerHTML = element.alt; // Uses the alt text as a caption
}

function closeModal() {
  document.getElementById("imageModal").style.display = "none";
}
