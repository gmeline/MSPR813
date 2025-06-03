document.addEventListener("DOMContentLoaded", () => {
    const items = document.getElementsByClassName("openable-item");
    const modal = document.getElementById("dialog-modal");
    const closeButton = document.getElementById("close-modal-button");
    Array.from(items).forEach((item, index) => {
        item.addEventListener("click", (e) => {
            e.preventDefault();
            const img = document.getElementsByTagName("img")[index];
            const imgClone = img.cloneNode(true);
            imgClone.classList.add("modal-image");
            modal.appendChild(imgClone);
            modal.showModal();
        })

    });
         modal.addEventListener("close", () => { closeModal()
    });
         closeButton.addEventListener("click",() => {
             closeModal()
             modal.close()
         })
         function closeModal() {
                const img = document.getElementsByClassName('modal-image')[0];
            modal.removeChild(img);

         }
});