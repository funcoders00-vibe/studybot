import { useState, useRef, useEffect } from 'react'

const QUICK_ACTIONS = [
  { label: 'Explain Simply', prompt: 'Explain this in simple, beginner-friendly language.' },
  { label: 'Summarize', prompt: 'Summarize the key points and important facts from this.' },
  { label: 'Generate MCQs', prompt: 'Generate 10 multiple choice questions based on this.' },
  { label: 'Practice', prompt: 'I want to practice 10 questions on this topic.' },
  { label: 'Mock Test', prompt: 'Conduct a 30-minute mock test on this topic.' },
]

export default function ChatInput({ onSendMessage, disabled }) {
  const [text, setText] = useState('')
  const textareaRef = useRef(null)

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`
    }
  }, [text])

  function handleSend() {
    const trimmed = text.trim()
    if (!trimmed || disabled) return
    onSendMessage(trimmed)
    setText('')
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  function handleQuickAction(actionPrompt) {
    if (disabled) return
    if (text.trim()) {
      // If user typed/pasted text, append the instruction
      onSendMessage(`${text.trim()}\n\n${actionPrompt}`)
      setText('')
    } else {
      // Send the prompt directly referencing prior chat context
      onSendMessage(actionPrompt)
    }
  }

  return (
    <div className="chat-input-container">
      <div className="chat-quick-actions">
        {QUICK_ACTIONS.map((qa) => (
          <button
            key={qa.label}
            type="button"
            className="quick-action-pill"
            onClick={() => handleQuickAction(qa.prompt)}
            disabled={disabled}
          >
            {qa.label}
          </button>
        ))}
      </div>

      <div className="chat-input-box">
        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question or paste your study content..."
          disabled={disabled}
          rows={1}
        />
        <button
          type="button"
          className="chat-send-btn primary"
          onClick={handleSend}
          disabled={disabled || !text.trim()}
        >
          {disabled ? 'Thinking…' : 'Send →'}
        </button>
      </div>
    </div>
  )
}
