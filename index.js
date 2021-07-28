///////////////////////
// PDB FILE RENUMBER //
///////////////////////

const inputFile = document.getElementById('renumber-file');
const inputResidue = document.getElementById('renumber-start');
const inputSubmit = document.getElementById('renumber-submit');
const inputResult = document.getElementById('renumber-output');
const fileCopy = document.getElementById('renumber-copy');

// check to make sure that inputs are valid
// TODO: check pdbFile is valid
const checkInput = (startResidue, pdbFile) => {
    if (!/[0-9]/.test(startResidue)) {
        // not a valid number
        console.log(
            `${startResidue} is an invalid residue number. Please input in an integer x_x`
        );
    } else {
        startResidue = parseInt(startResidue); // turn it into a number
    }
    return [startResidue, pdbFile];
};

// renumbers the PDB
const renumberPDB = (startResidue, pdbFile) => {
    [startResidue, pdbFile] = checkInput(startResidue, pdbFile);
    startResidue--;
    currentResidue = startResidue;
    previousResidue = 0;

    let pdbFileSplit = pdbFile.split('\n');
    let pdbFileRenumb = [];

    for (line of pdbFileSplit) {
        if (
            line.startsWith('ATOM') ||
            line.startsWith('HETATM') ||
            line.startsWith('TER')
        ) {
            if (line.slice(22, 26) != previousResidue) {
                previousResidue = line.slice(22, 26);
                currentResidue++;
            }
            pdbFileRenumb.push(
                line.slice(0, 22) +
                    currentResidue.toString().padStart(4, ' ') +
                    line.slice(26)
            );
        } else {
            pdbFileRenumb.push(line);
        }
    }

    pdbFileRenumb = pdbFileRenumb.join('\n');
    return pdbFileRenumb;
};

// reads the file input in the form
inputFile.addEventListener(
    'change',
    (event) => {
        const reader = new FileReader();
        reader.onload = (event) => {
            window.fileCurrent = event.target.result;
        };
        let file = event.target.files[0];
        reader.readAsText(file);
    },
    false
);

// script after submission
inputSubmit.onclick = () => {
    window.startingResidue = parseInt(inputResidue.value);
    let [startResidue, pdbFile] = checkInput(
        window.startingResidue,
        window.fileCurrent
    );
    let pdbFileRenumb = renumberPDB(startResidue, pdbFile);
    inputResult.innerHTML = pdbFileRenumb;
    fileCopy.style.display = 'block';
};

// copy script
fileCopy.onclick = () => {
    let copyRange = document.createRange();
    copyRange.selectNode(inputResult);
    window.getSelection().addRange(copyRange);
    document.execCommand('copy');
    window.getSelection().removeRange(copyRange);
};

///////////////
// AESTHETIC //
///////////////

const fileInterface = document.querySelector(
    '#file-interface input[type=file]'
);
const fileName = document.querySelector('#file-interface .file-name');

fileInterface.onchange = () => {
    if (fileInterface.files.length > 0) {
        fileName.textContent = fileInterface.files[0].name;
    } else {
        fileNamee.textContent = 'No file uploaded';
    }
};

// /\__/\
// (=o.o=)
// |/--\|
// (")-(")
