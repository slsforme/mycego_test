function removeLabels() {
    const labels = document.getElementsByTagName('label')
    for (let i = 0; i < labels.length; i++){
        labels[i].remove();
    }
}

removeLabels();