const resumeStack = [];
const jdStack = [];

// Updates the visual list of files on the UI
function updateFileList(listId, stack, inputType) {
  const list = document.getElementById(listId);
  list.innerHTML = '';
  
  stack.forEach((file, index) => {
    const li = document.createElement('li');
    li.className = 'flex justify-between items-center bg-gray-100 px-4 py-1 mb-1 rounded';
    li.innerHTML = `
      <span>${file.name}</span>
      <button type="button"
        class="remove-btn text-red-400 text-xs font-medium"
        onclick="removeFile(event, '${inputType}', ${index})">x</button>`;
    list.appendChild(li);
  });
}

// Removes a specific file from the stack and updates the UI
function removeFile(event, type, index) {
  // Prevent parent dropzone from triggering file input when clicking remove
  event.stopPropagation(); 

  if (type === 'resume') {
    resumeStack.splice(index, 1);
  } else {
    jdStack.splice(index, 1);
  }

  const listId = type === 'resume' ? 'resumeList' : 'jdList';
  const stack = type === 'resume' ? resumeStack : jdStack;
  
  updateFileList(listId, stack, type);
  checkFiles();
}

// Enables or disables the submit button based on file presence
function checkFiles() {
  const submitBtn = document.getElementById("submitBtn");

  if (resumeStack.length > 0 && jdStack.length > 0) {
    submitBtn.disabled = false;
    submitBtn.classList.remove("bg-gray-400", "cursor-not-allowed");
    submitBtn.classList.add(
      "bg-blue-500", 
      "hover:bg-white", 
      "hover:text-black", 
      "hover:border", 
      "hover:border-black", 
      "cursor-pointer"
    );
  } else {
    submitBtn.disabled = true;
    submitBtn.classList.add("bg-gray-400", "cursor-not-allowed");
    submitBtn.classList.remove(
      "bg-blue-500", 
      "hover:bg-white", 
      "hover:text-black", 
      "hover:border", 
      "hover:border-black", 
      "cursor-pointer"
    );
  }
}

// Event Listeners for Manual Selection
document.getElementById('resumeDrop').addEventListener('click', (e) => {
  if (!e.target.classList.contains('remove-btn')) {
    document.getElementById('resumeInput').click();
  }
});

document.getElementById('jdDrop').addEventListener('click', (e) => {
  if (!e.target.classList.contains('remove-btn')) {
    document.getElementById('jdInput').click();
  }
});

// Input Change Listeners
document.getElementById('resumeInput').addEventListener('change', (e) => {
  for (let file of e.target.files) resumeStack.push(file);
  updateFileList('resumeList', resumeStack, 'resume');
  checkFiles();
});

document.getElementById('jdInput').addEventListener('change', (e) => {
  for (let file of e.target.files) jdStack.push(file);
  updateFileList('jdList', jdStack, 'jd');
  checkFiles();
});

// Initializes Drag and Drop functionality for a given zone
function makeDropZone(id, stack, listId, inputType) {
  const dropZone = document.getElementById(id);

  dropZone.addEventListener('dragover', e => {
    e.preventDefault();
    dropZone.classList.add('bg-blue-50');
  });

  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('bg-blue-50');
  });

  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    dropZone.classList.remove('bg-blue-50');
    
    const files = Array.from(e.dataTransfer.files);
    files.forEach(file => stack.push(file));
    
    updateFileList(listId, stack, inputType);
    checkFiles();
  });
}

// Initialize Drop Zones
makeDropZone('resumeDrop', resumeStack, 'resumeList', 'resume');
makeDropZone('jdDrop', jdStack, 'jdList', 'jd');

// Form Submission Handling
document.getElementById('uploadForm').addEventListener('submit', function (e) {
  e.preventDefault();
  
  const formData = new FormData();
  resumeStack.forEach(file => formData.append('resumes', file));
  jdStack.forEach(file => formData.append('jds', file));

  fetch('/upload', {
    method: 'POST',
    body: formData
  }).then(res => {
    if (res.redirected) {
      window.location.href = res.url;
    }
  }).catch(err => {
    console.error("Upload failed:", err);
  });
});
