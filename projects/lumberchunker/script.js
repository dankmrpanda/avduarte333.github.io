// Embedded quiz data with chunk breaks
const QUIZ_DATA = {
  sentences: [
    { id: 0, text: '"What about a story?" I said.' },
    { id: 1, text: '"Could you very sweetly tell Winnie-the-Pooh one?"' },
    { id: 2, text: '"I suppose I could," I said. "What sort of stories does he like?"' },
    { id: 3, text: '"About himself. Because he\'s that sort of Bear."' },
    { id: 4, text: '"Oh, I see."' },
    { id: 5, text: '"So could you very sweetly?"' },
    { id: 6, text: '"I\'ll try," I said.' },
    { id: 7, text: 'So I tried.' },
    { id: 8, text: 'Once upon a time, a very long time ago now, about last Friday, Winnie-the-Pooh lived in a forest all by himself under the name of Sanders.' },
    { id: 9, text: '"What does \'under the name\' mean?" asked Christopher Robin.' }
  ],
  // Model's answer: breaks after sentences 7 (creating 2 chunks)
  modelBreaks: [7],
  chunks: [
    {
      id: 1,
      name: "Dialogue Setup",
      sentences: [0, 1, 2, 3, 4, 5, 6, 7],
      reasoning: "These sentences form a complete dialogue where Christopher Robin asks for a story about Winnie-the-Pooh. They establish the context and setup for what follows, showing the conversational flow from request to agreement."
    },
    {
      id: 2,
      name: "Story Beginning",
      sentences: [8, 9],
      reasoning: "These sentences transition from the setup dialogue into the actual storytelling. The narrator begins the story with a classic fairy tale opening, immediately followed by Christopher Robin's interruption with a question about the story."
    }
  ]
};

class TextChunkingQuiz {
  constructor() {
    this.quizData = QUIZ_DATA;
    this.userBreaks = new Set(); // Stores indices where user placed breaks
    this.init();
  }

  init() {
    this.renderInterface();
    this.setupEventListeners();
  }

  renderInterface() {
    this.renderSentences();
  }

  renderSentences() {
    const container = d3.select('#sentencesContainer');
    container.selectAll('*').remove();

    this.quizData.sentences.forEach((sentence, index) => {
      // Add sentence
      container.append('div')
        .attr('class', 'sentence')
        .attr('data-id', sentence.id)
        .text(sentence.text);

      // Add break indicator after sentence (except last one)
      if (index < this.quizData.sentences.length - 1) {
        const breakDiv = container.append('div')
          .attr('class', 'break-indicator')
          .attr('data-after-id', sentence.id);

        breakDiv.append('div')
          .attr('class', 'break-line')
          .on('click', () => this.toggleBreak(sentence.id));

        breakDiv.append('div')
          .attr('class', 'break-button')
          .html('···')
          .on('click', () => this.toggleBreak(sentence.id));
      }
    });

    this.updateBreakStyles();
  }

  toggleBreak(afterSentenceId) {
    if (this.userBreaks.has(afterSentenceId)) {
      this.userBreaks.delete(afterSentenceId);
    } else {
      this.userBreaks.add(afterSentenceId);
    }
    this.updateBreakStyles();
  }

  updateBreakStyles() {
    d3.selectAll('.break-indicator').each((d, i, nodes) => {
      const element = d3.select(nodes[i]);
      const afterId = parseInt(element.attr('data-after-id'));
      
      if (this.userBreaks.has(afterId)) {
        element.classed('active', true);
      } else {
        element.classed('active', false);
      }
    });

    // Update chunk highlighting
    const chunks = this.getUserChunks();
    d3.selectAll('.sentence').each((d, i, nodes) => {
      const element = d3.select(nodes[i]);
      const sentenceId = parseInt(element.attr('data-id'));
      
      // Remove all chunk classes
      element.attr('class', 'sentence');
      
      // Find which chunk this sentence belongs to
      chunks.forEach((chunk, chunkIndex) => {
        if (chunk.includes(sentenceId)) {
          element.classed(`chunk-${chunkIndex + 1}`, true);
        }
      });
    });
  }

  getUserChunks() {
    const chunks = [];
    let currentChunk = [];
    
    this.quizData.sentences.forEach((sentence, index) => {
      currentChunk.push(sentence.id);
      
      // If there's a break after this sentence, start new chunk
      if (this.userBreaks.has(sentence.id)) {
        chunks.push([...currentChunk]);
        currentChunk = [];
      }
    });
    
    // Add remaining sentences as final chunk
    if (currentChunk.length > 0) {
      chunks.push(currentChunk);
    }
    
    return chunks;
  }

  getModelChunks() {
    const chunks = [];
    let currentChunk = [];
    
    this.quizData.sentences.forEach((sentence, index) => {
      currentChunk.push(sentence.id);
      
      // If there's a break after this sentence in model's answer
      if (this.quizData.modelBreaks.includes(sentence.id)) {
        chunks.push([...currentChunk]);
        currentChunk = [];
      }
    });
    
    // Add remaining sentences as final chunk
    if (currentChunk.length > 0) {
      chunks.push(currentChunk);
    }
    
    return chunks;
  }

  setupEventListeners() {
    d3.select('#checkBtn').on('click', () => this.showComparison());
    d3.select('#resetBtn').on('click', () => this.resetQuiz());
  }

  showComparison() {
    const container = d3.select('#comparisonContainer');
    const content = d3.select('#comparisonContent');
    const sentencesContainer = d3.select('#sentencesContainer');
    const controls = d3.select('.controls');
    
    // Start fade out animation
    sentencesContainer.classed('fade-out', true);
    controls.classed('fade-out', true);
    
    // Wait for fade out to complete, then switch content
    setTimeout(() => {
      // Hide quiz interface
      sentencesContainer.classed('hidden', true);
      controls.classed('hidden', true);
      
      // Clear and prepare comparison content
      content.selectAll('*').remove();

    const userChunks = this.getUserChunks();
    const modelChunks = this.getModelChunks();

    // Create comparison header
    const header = content.append('div')
      .attr('class', 'comparison-summary');
    
    header.append('p')
      .html(`<strong>Your chunking:</strong> ${userChunks.length} chunks<br><strong>Model's chunking:</strong> ${modelChunks.length} chunks`);

    // Show side-by-side comparison
    const row = content.append('div')
      .attr('class', 'comparison-row');

    // Your chunks column
    const userCol = row.append('div')
      .attr('class', 'comparison-col');
    userCol.append('h3').text('Your Chunks');
    
    userChunks.forEach((chunk, index) => {
      const chunkDiv = userCol.append('div')
        .attr('class', `chunk-display user-chunk-${index + 1}`);
      
      chunkDiv.append('h4').text(`Chunk ${index + 1}`);
      
      const sentencesDiv = chunkDiv.append('div')
        .attr('class', 'chunk-sentences');
      
      chunk.forEach(sentenceId => {
        const sentence = this.quizData.sentences.find(s => s.id === sentenceId);
        if (sentence) {
          sentencesDiv.append('p')
            .attr('class', 'chunk-sentence')
            .text(sentence.text);
        }
      });
    });

    // Model's chunks column
    const modelCol = row.append('div')
      .attr('class', 'comparison-col');
    modelCol.append('h3').text('Model\'s Chunks');
    
    modelChunks.forEach((chunk, index) => {
      const chunkDiv = modelCol.append('div')
        .attr('class', `chunk-display model-chunk-${index + 1}`);
      
      const chunkInfo = this.quizData.chunks[index];
      chunkDiv.append('h4').text(`Chunk ${index + 1}: ${chunkInfo.name}`);
      
      const sentencesDiv = chunkDiv.append('div')
        .attr('class', 'chunk-sentences');
      
      chunk.forEach(sentenceId => {
        const sentence = this.quizData.sentences.find(s => s.id === sentenceId);
        if (sentence) {
          sentencesDiv.append('p')
            .attr('class', 'chunk-sentence')
            .text(sentence.text);
        }
      });

      // Add reasoning
      if (chunkInfo.reasoning) {
        chunkDiv.append('div')
          .attr('class', 'reasoning-box')
          .html(`<strong>Why these belong together:</strong><br>${chunkInfo.reasoning}`);
      }
    });

    // Calculate accuracy
    const accuracy = this.calculateAccuracy(userChunks, modelChunks);
    
    content.append('div')
      .attr('class', 'accuracy-box')
      .html(`<h4>Match Score: ${accuracy}%</h4><p>This shows how closely your chunking matches the model's segmentation.</p>`);

      // Add back button at the bottom
      const bottomButton = content.append('div')
        .attr('class', 'action-buttons')
        .style('margin-top', '20px')
        .style('text-align', 'center');
      
      bottomButton.append('button')
        .attr('class', 'btn back-btn')
        .text('← Back to Quiz')
        .on('click', () => this.hideComparison());

      // Show container and trigger fade in
      container.classed('show', true);
      
      // Trigger fade in animation
      setTimeout(() => {
        container.classed('fade-in', true);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }, 50);
    }, 400); // Match the CSS transition duration (400ms)
  }

  hideComparison() {
    const container = d3.select('#comparisonContainer');
    const sentencesContainer = d3.select('#sentencesContainer');
    const controls = d3.select('.controls');
    
    // Start fade out of comparison
    container.classed('fade-in', false);
    
    setTimeout(() => {
      // Hide comparison
      container.classed('show', false);
      
      // Show quiz interface
      sentencesContainer.classed('hidden', false);
      controls.classed('hidden', false);
      
      // Remove fade-out classes to trigger fade in
      setTimeout(() => {
        sentencesContainer.classed('fade-out', false);
        controls.classed('fade-out', false);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }, 50);
    }, 400); // Match the CSS transition duration
  }

  calculateAccuracy(userChunks, modelChunks) {
    // Simple accuracy: check if breaks are in same positions
    const userBreakSet = new Set(this.userBreaks);
    const modelBreakSet = new Set(this.quizData.modelBreaks);
    
    const totalPossibleBreaks = this.quizData.sentences.length - 1;
    let correctBreaks = 0;
    
    for (let i = 0; i < this.quizData.sentences.length - 1; i++) {
      const sentenceId = this.quizData.sentences[i].id;
      const userHasBreak = userBreakSet.has(sentenceId);
      const modelHasBreak = modelBreakSet.has(sentenceId);
      
      if (userHasBreak === modelHasBreak) {
        correctBreaks++;
      }
    }
    
    return Math.round((correctBreaks / totalPossibleBreaks) * 100);
  }

  resetQuiz() {
    const container = d3.select('#comparisonContainer');
    const sentencesContainer = d3.select('#sentencesContainer');
    const controls = d3.select('.controls');
    
    // If comparison is showing, hide it first
    if (container.classed('show')) {
      this.hideComparison();
      // Wait for animation to complete before resetting
      setTimeout(() => {
        this.userBreaks.clear();
        this.updateBreakStyles();
      }, 500);
    } else {
      // Just reset normally
      this.userBreaks.clear();
      container.classed('show', false).classed('fade-in', false);
      sentencesContainer.classed('hidden', false).classed('fade-out', false);
      controls.classed('hidden', false).classed('fade-out', false);
      this.updateBreakStyles();
    }
  }
}

// Initialize quiz when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new TextChunkingQuiz();
});
