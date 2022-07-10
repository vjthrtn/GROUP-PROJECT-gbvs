function deleteNote(noteId) {
    fetch("/delete-note", {
    method: 'POST',
    body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
    window.location.href = "/";
    });
}

function copy() {
    /* Get the text field */
    var copyText = document.getElementById("urlResult");
  
    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /* For mobile devices */
  
     /* Copy the text inside the text field */
    navigator.clipboard.writeText(copyText.value);
  
    /* Alert the copied text */
    alert("Copied to clipboard! Copied:" + copyText.value);
  }