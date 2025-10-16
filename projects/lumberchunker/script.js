// Embedded quiz data with multiple choice options
const QUIZ_DATA = {
  passage: [
    '"What about a story?" I said.',
    '"Could you very sweetly tell Winnie-the-Pooh one?"',
    '"I suppose I could," I said. "What sort of stories does he like?"',
    '"About himself. Because he\'s that sort of Bear."',
    '"Oh, I see."',
    '"So could you very sweetly?"',
    '"I\'ll try," I said.',
    'So I tried.',
    'Once upon a time, a very long time ago now, about last Friday, Winnie-the-Pooh lived in a forest all by himself under the name of Sanders.',
    '"What does \'under the name\' mean?" asked Christopher Robin.'
  ],
  question: "How should this passage be segmented for optimal semantic chunking?",
  options: [
    {
      id: 'A',
      label: 'Split after every sentence (10 chunks)',
      breaks: [0, 1, 2, 3, 4, 5, 6, 7, 8],
      chunks: [
        { sentences: [0], name: "Chunk 1" },
        { sentences: [1], name: "Chunk 2" },
        { sentences: [2], name: "Chunk 3" },
        { sentences: [3], name: "Chunk 4" },
        { sentences: [4], name: "Chunk 5" },
        { sentences: [5], name: "Chunk 6" },
        { sentences: [6], name: "Chunk 7" },
        { sentences: [7], name: "Chunk 8" },
        { sentences: [8], name: "Chunk 9" },
        { sentences: [9], name: "Chunk 10" }
      ],
      feedback: "This creates too many tiny chunks! Each sentence is isolated, losing the semantic connections between related dialogue. This approach would make retrieval inefficient and fail to capture the conversational flow."
    },
    {
      id: 'B',
      label: 'Keep everything together (1 chunk)',
      breaks: [],
      chunks: [
        { sentences: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], name: "Entire Passage" }
      ],
      feedback: "This treats the entire passage as one chunk, mixing two distinct sections: the dialogue setup and the story beginning. The shift from meta-conversation to storytelling represents a clear semantic boundary that should be captured."
    },
    {
      id: 'C',
      label: 'Split between dialogue and story (2 chunks)',
      breaks: [7],
      chunks: [
        { 
          sentences: [0, 1, 2, 3, 4, 5, 6, 7], 
          name: "Dialogue Setup",
          reasoning: "These sentences form a complete dialogue where Christopher Robin asks for a story about Winnie-the-Pooh. They establish the context and setup for what follows, showing the conversational flow from request to agreement."
        },
        { 
          sentences: [8, 9], 
          name: "Story Beginning",
          reasoning: "These sentences transition from the setup dialogue into the actual storytelling. The narrator begins the story with a classic fairy tale opening, immediately followed by Christopher Robin's interruption with a question about the story."
        }
      ],
      feedback: "Correct! This segmentation recognizes the semantic boundary between the meta-dialogue (discussing what story to tell) and the actual storytelling. The first chunk captures the complete request-and-agreement exchange, while the second chunk begins the narrative with its classic opening and immediate interruption.",
      isCorrect: true
    }
  ],
  correctAnswer: 'C'
};

class TextChunkingQuiz {
  constructor() {
    this.quizData = QUIZ_DATA;
    this.selectedOption = null;
    this.hasSubmitted = false;
    this.init();
  }

  init() {
    this.renderQuiz();
    this.setupEventListeners();
  }

  renderQuiz() {
    this.renderPassage();
    this.renderOptions();
  }

  renderPassage() {
    const container = d3.select('#passageContainer');
    container.selectAll('*').remove();

    this.quizData.passage.forEach((sentence, index) => {
      container.append('p')
        .attr('class', 'passage-sentence')
        .attr('data-id', index)
        .text(sentence);
    });
  }

  renderOptions() {
    const container = d3.select('#optionsContainer');
    container.selectAll('*').remove();

    this.quizData.options.forEach(option => {
      const optionDiv = container.append('div')
        .attr('class', 'option-card')
        .attr('data-option-id', option.id)
        .on('click', () => this.selectOption(option.id));

      const header = optionDiv.append('div')
        .attr('class', 'option-header');

      header.append('input')
        .attr('type', 'radio')
        .attr('name', 'chunking-option')
        .attr('id', `option-${option.id}`)
        .attr('value', option.id)
        .property('checked', this.selectedOption === option.id);

      header.append('label')
        .attr('for', `option-${option.id}`)
        .html(`<strong>Option ${option.id}:</strong> ${option.label}`);

      // Preview chunks
      const preview = optionDiv.append('div')
        .attr('class', 'chunk-preview');

      option.chunks.forEach((chunk, idx) => {
        const chunkDiv = preview.append('div')
          .attr('class', `chunk-preview-item chunk-${(idx % 5) + 1}`);

        chunkDiv.append('div')
          .attr('class', 'chunk-name')
          .text(chunk.name);

        const sentences = chunkDiv.append('div')
          .attr('class', 'chunk-sentences-preview');

        chunk.sentences.forEach(sentenceIdx => {
          sentences.append('p')
            .attr('class', 'preview-sentence')
            .text(this.quizData.passage[sentenceIdx]);
        });
      });
    });
  }

  selectOption(optionId) {
    // Allow selection change at any time
    this.selectedOption = optionId;
    
    // Update visual selection
    d3.selectAll('.option-card').classed('selected', false);
    d3.select(`.option-card[data-option-id="${optionId}"]`).classed('selected', true);
    
    // Update radio button
    d3.selectAll('input[name="chunking-option"]').property('checked', false);
    d3.select(`#option-${optionId}`).property('checked', true);
    
    // If already submitted, automatically resubmit with new selection
    if (this.hasSubmitted) {
      this.hasSubmitted = false;
      this.submitAnswer();
    }
  }

  setupEventListeners() {
    d3.select('#submitBtn').on('click', () => this.submitAnswer());
  }

  submitAnswer() {
    if (!this.selectedOption) {
      alert('Please select an option before submitting!');
      return;
    }

    if (this.hasSubmitted) return; // Already submitted

    this.hasSubmitted = true;
    this.showResults();
  }

  showResults() {
    const resultsContainer = d3.select('#resultsContainer');
    const quizContent = d3.select('.quiz-content');
    const controls = d3.select('.controls');

    // Fade out quiz
    quizContent.classed('fade-out', true);
    controls.classed('fade-out', true);

    setTimeout(() => {
      quizContent.classed('hidden', true);
      controls.classed('hidden', true);

      // Clear and build results
      resultsContainer.selectAll('*').remove();

      const selectedOptionData = this.quizData.options.find(opt => opt.id === this.selectedOption);
      const isCorrect = selectedOptionData.isCorrect || false;

      // Result header
      const header = resultsContainer.append('div')
        .attr('class', `result-header ${isCorrect ? 'correct' : 'incorrect'}`);

      header.append('h2')
        .text(isCorrect ? 'Correct!' : 'Not Quite');

      header.append('p')
        .text(isCorrect ? 
          'You identified the optimal semantic segmentation!' : 
          'Let\'s review why this segmentation isn\'t ideal.');

      // Show selected answer
      const selectedSection = resultsContainer.append('div')
        .attr('class', 'result-section');

      selectedSection.append('h3')
        .html(`Your Answer: <span class="option-label">Option ${this.selectedOption}</span>`);

      selectedSection.append('div')
        .attr('class', 'feedback-box')
        .html(selectedOptionData.feedback);

      // Show selected option's chunks
      const chunksDiv = selectedSection.append('div')
        .attr('class', 'chunks-display');

      selectedOptionData.chunks.forEach((chunk, idx) => {
        const chunkDiv = chunksDiv.append('div')
          .attr('class', 'chunk-display');

        chunkDiv.append('h4')
          .text(chunk.name);

        const sentencesDiv = chunkDiv.append('div')
          .attr('class', 'chunk-sentences');

        chunk.sentences.forEach(sentenceIdx => {
          sentencesDiv.append('p')
            .attr('class', `chunk-sentence chunk-${(idx % 5) + 1}`)
            .text(this.quizData.passage[sentenceIdx]);
        });

        if (chunk.reasoning) {
          chunkDiv.append('div')
            .attr('class', 'reasoning-box')
            .html(`<strong>Why these belong together:</strong><br>${chunk.reasoning}`);
        }
      });

      // If wrong, show correct answer
      if (!isCorrect) {
        const correctSection = resultsContainer.append('div')
          .attr('class', 'result-section correct-answer-section');

        correctSection.append('h3')
          .html(`Correct Answer: <span class="option-label">Option ${this.quizData.correctAnswer}</span>`);

        const correctOption = this.quizData.options.find(opt => opt.id === this.quizData.correctAnswer);

        correctSection.append('div')
          .attr('class', 'feedback-box correct-feedback')
          .html(correctOption.feedback);

        // Show correct chunks
        const correctChunksDiv = correctSection.append('div')
          .attr('class', 'chunks-display');

        correctOption.chunks.forEach((chunk, idx) => {
          const chunkDiv = correctChunksDiv.append('div')
            .attr('class', 'chunk-display');

          chunkDiv.append('h4')
            .text(chunk.name);

          const sentencesDiv = chunkDiv.append('div')
            .attr('class', 'chunk-sentences');

          chunk.sentences.forEach(sentenceIdx => {
            sentencesDiv.append('p')
              .attr('class', `chunk-sentence chunk-${(idx % 5) + 1}`)
              .text(this.quizData.passage[sentenceIdx]);
          });

          if (chunk.reasoning) {
            chunkDiv.append('div')
              .attr('class', 'reasoning-box')
              .html(`<strong>Why these belong together:</strong><br>${chunk.reasoning}`);
          }
        });
      }

      // Back button
      const backButton = resultsContainer.append('div')
        .attr('class', 'action-buttons')
        .style('margin-top', '30px')
        .style('text-align', 'center');

      backButton.append('button')
        .attr('class', 'btn back-btn')
        .text('← Back to Quiz')
        .on('click', () => this.hideResults());

      // Show results with fade in
      resultsContainer.classed('show', true);
      setTimeout(() => {
        resultsContainer.classed('fade-in', true);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }, 50);
    }, 400);
  }

  hideResults() {
    const resultsContainer = d3.select('#resultsContainer');
    const quizContent = d3.select('.quiz-content');
    const controls = d3.select('.controls');

    // Fade out results
    resultsContainer.classed('fade-in', false);

    setTimeout(() => {
      resultsContainer.classed('show', false);

      // Show quiz
      quizContent.classed('hidden', false);
      controls.classed('hidden', false);

      setTimeout(() => {
        quizContent.classed('fade-out', false);
        controls.classed('fade-out', false);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }, 50);
    }, 400);
  }
}

// Initialize quiz when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new TextChunkingQuiz();
});

