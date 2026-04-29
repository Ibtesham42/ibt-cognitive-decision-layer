import { useState } from 'react'
import axios from 'axios'

function App() {
  const [input, setInput] = useState('')
  const [mode, setMode] = useState('reason') // 'parse' or 'reason'
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      if (mode === 'parse') {
        const response = await axios.post('/api/v1/parse', {
          text: input,
          output_format: 'full'
        })
        setResult(response.data)
      } else {
        const response = await axios.post('/api/v1/reason', {
          problem: input,
          depth: 5,
          max_iterations: 5
        })
        setResult(response.data)
      }
    } catch (err) {
      setError(err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-blue-400 mb-2">
            Decision Layer AI
          </h1>
          <p className="text-gray-400">
            Universal Symbolic Language & Deep Reasoning Engine
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Input Panel */}
          <div className="lg:col-span-1">
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
              <h2 className="text-xl font-semibold mb-4">Input</h2>
              
              <div className="flex gap-2 mb-4">
                <button
                  onClick={() => setMode('parse')}
                  className={`flex-1 py-2 px-4 rounded ${
                    mode === 'parse' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  Parse
                </button>
                <button
                  onClick={() => setMode('reason')}
                  className={`flex-1 py-2 px-4 rounded ${
                    mode === 'reason' 
                      ? 'bg-green-600 text-white' 
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  Reason
                </button>
              </div>

              <form onSubmit={handleSubmit}>
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder={
                    mode === 'parse' 
                      ? 'Enter text to parse into symbols...' 
                      : 'Enter a problem to reason about...'
                  }
                  className="w-full h-32 bg-gray-700 border border-gray-600 rounded p-3 text-white focus:outline-none focus:border-blue-500 mb-4"
                />
                <button
                  type="submit"
                  disabled={loading || !input.trim()}
                  className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-green-600 rounded font-semibold hover:from-blue-700 hover:to-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
                >
                  {loading ? 'Processing...' : 'Execute'}
                </button>
              </form>

              {error && (
                <div className="mt-4 p-3 bg-red-900/50 border border-red-700 rounded text-red-300">
                  {error}
                </div>
              )}
            </div>

            {/* Examples */}
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg mt-6">
              <h3 className="text-lg font-semibold mb-3">Examples</h3>
              <div className="space-y-2 text-sm text-gray-400">
                {mode === 'parse' ? (
                  <>
                    <p className="hover:text-white cursor-pointer" onClick={() => setInput('The robot moves quickly to the left')}>
                      • The robot moves quickly to the left
                    </p>
                    <p className="hover:text-white cursor-pointer" onClick={() => setInput('If temperature increases then pressure will rise')}>
                      • If temperature increases then pressure will rise
                    </p>
                    <p className="hover:text-white cursor-pointer" onClick={() => setInput('All students must complete the assignment before tomorrow')}>
                      • All students must complete before tomorrow
                    </p>
                  </>
                ) : (
                  <>
                    <p className="hover:text-white cursor-pointer" onClick={() => setInput('How to reduce system latency?')}>
                      • How to reduce system latency?
                    </p>
                    <p className="hover:text-white cursor-pointer" onClick={() => setInput('Why is customer satisfaction declining?')}>
                      • Why is customer satisfaction declining?
                    </p>
                    <p className="hover:text-white cursor-pointer" onClick={() => setInput('What is the optimal resource allocation strategy?')}>
                      • What is the optimal resource allocation?
                    </p>
                  </>
                )}
              </div>
            </div>
          </div>

          {/* Results Panel */}
          <div className="lg:col-span-2">
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg min-h-[600px]">
              <h2 className="text-xl font-semibold mb-4">Results</h2>
              
              {!result && !loading && (
                <div className="flex items-center justify-center h-96 text-gray-500">
                  <p>Enter input and click Execute to see results</p>
                </div>
              )}

              {loading && (
                <div className="flex items-center justify-center h-96">
                  <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
                </div>
              )}

              {result && mode === 'parse' && (
                <div className="space-y-4">
                  <div className="bg-gray-700 rounded p-4">
                    <h3 className="font-semibold text-blue-400 mb-2">Symbolic Representation</h3>
                    <code className="text-sm text-green-400 block whitespace-pre-wrap">
                      {result.symbols?.map(s => `[${s.type}:${s.value}]`).join(' ')}
                    </code>
                  </div>
                  
                  <div className="bg-gray-700 rounded p-4">
                    <h3 className="font-semibold text-blue-400 mb-2">Structure</h3>
                    <pre className="text-xs text-gray-300 overflow-auto max-h-64">
                      {JSON.stringify(result.structure, null, 2)}
                    </pre>
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div className="bg-gray-700 rounded p-3">
                      <span className="text-gray-400">Processing Time:</span>
                      <span className="ml-2 text-white">{result.processing_time_ms}ms</span>
                    </div>
                    <div className="bg-gray-700 rounded p-3">
                      <span className="text-gray-400">Symbols Found:</span>
                      <span className="ml-2 text-white">{result.symbols?.length || 0}</span>
                    </div>
                  </div>
                </div>
              )}

              {result && mode === 'reason' && (
                <div className="space-y-4">
                  {result.final_solution && (
                    <div className="bg-gradient-to-r from-green-900/50 to-blue-900/50 border border-green-700 rounded p-4">
                      <h3 className="font-semibold text-green-400 mb-2">🏆 Best Solution</h3>
                      <p className="text-white mb-3">{result.final_solution.description}</p>
                      <div className="grid grid-cols-3 gap-2 text-sm">
                        <div className="bg-gray-800 rounded p-2 text-center">
                          <div className="text-gray-400">Feasibility</div>
                          <div className="text-green-400 font-bold">
                            {(result.final_solution.feasibility_score * 100).toFixed(0)}%
                          </div>
                        </div>
                        <div className="bg-gray-800 rounded p-2 text-center">
                          <div className="text-gray-400">Optimality</div>
                          <div className="text-blue-400 font-bold">
                            {(result.final_solution.optimality_score * 100).toFixed(0)}%
                          </div>
                        </div>
                        <div className="bg-gray-800 rounded p-2 text-center">
                          <div className="text-gray-400">Confidence</div>
                          <div className="text-purple-400 font-bold">
                            {(result.final_solution.confidence * 100).toFixed(0)}%
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="bg-gray-700 rounded p-4">
                    <h3 className="font-semibold text-blue-400 mb-2">📊 Meta-Evaluation</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                      {Object.entries(result.meta_evaluation || {})
                        .filter(([key]) => key !== 'recommendations')
                        .map(([key, value]) => (
                          <div key={key} className="bg-gray-800 rounded p-2">
                            <div className="text-gray-400 capitalize">{key.replace('_', ' ')}</div>
                            <div className="text-white font-semibold">
                              {typeof value === 'number' ? value.toFixed(3) : value}
                            </div>
                          </div>
                        ))}
                    </div>
                  </div>

                  <div className="bg-gray-700 rounded p-4">
                    <h3 className="font-semibold text-blue-400 mb-2">💡 Recommendations</h3>
                    <ul className="space-y-1 text-sm text-gray-300">
                      {(result.meta_evaluation?.recommendations || []).map((rec, idx) => (
                        <li key={idx} className="flex items-start">
                          <span className="text-green-400 mr-2">•</span>
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div className="bg-gray-700 rounded p-3">
                      <span className="text-gray-400">Iterations:</span>
                      <div className="text-white font-bold">{result.iterations}</div>
                    </div>
                    <div className="bg-gray-700 rounded p-3">
                      <span className="text-gray-400">Convergence:</span>
                      <div className={result.convergence_achieved ? 'text-green-400 font-bold' : 'text-yellow-400 font-bold'}>
                        {result.convergence_achieved ? 'Yes ✓' : 'No'}
                      </div>
                    </div>
                    <div className="bg-gray-700 rounded p-3">
                      <span className="text-gray-400">Time:</span>
                      <div className="text-white font-bold">{result.total_time_ms}ms</div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
