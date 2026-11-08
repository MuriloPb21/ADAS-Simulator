
import { useState, useEffect, useCallback } from 'react'
import './App.css'

function App() {
  const [dados, setDados] = useState({
    vel_atual: '',
    vel_frente: '',
    radar: '',
    lidar: '',
    camera: '',
    atrito: '0.7',
    nivel: '2',
    faixa_esq: '',
    faixa_dir: ''
  })

  const [resultado, setResultado] = useState(null)
  const [carregando, setCarregando] = useState(false)
  const [erro, setErro] = useState('')
  const [conexao, setConexao] = useState('DESCONECTADA')

  const [historico, setHistorico] = useState([])
  const [carregandoHistorico, setCarregandoHistorico] = useState(true)
  const [erroHistorico, setErroHistorico] = useState('')

  const [simulacoesExpandidas, setSimulacoesExpandidas] = useState([])

  function alternarDetalhes(id) {
  setSimulacoesExpandidas((atual) =>
    atual.includes(id)
      ? atual.filter((item) => item !== id)
      : [...atual, id]
  )
}

  const carregarHistorico = useCallback(async () => {
    setCarregandoHistorico(true)
    setErroHistorico('')

    try {
      const resposta = await fetch('http://127.0.0.1:8000/historico')

      if (!resposta.ok) {
        throw new Error('Não foi possível carregar o histórico.')
      }

      const dadosHistorico = await resposta.json()
      setHistorico(dadosHistorico)

    } catch (error) {
      setErroHistorico(error.message)
    } finally {
      setCarregandoHistorico(false)
    }
  }, [])

  useEffect(() => {
    async function verificarAPI() {
      try {
        const resposta = await fetch('http://127.0.0.1:8000/')

        if (!resposta.ok) {
          throw new Error('API indisponível')
        }

        setConexao('CONECTADA')
        await carregarHistorico()

      } catch {
        setConexao('DESCONECTADA')
        setCarregandoHistorico(false)
        setErroHistorico('Não foi possível conectar ao histórico.')
      }
    }

    verificarAPI()
  }, [carregarHistorico])

  function handleChange(event) {
    const { name, value } = event.target

    setDados({
      ...dados,
      [name]: value
    })
  }

  async function handleSubmit(event) {
    event.preventDefault()

    setCarregando(true)
    setErro('')
    setResultado(null)

    const dadosNumericos = Object.fromEntries(
      Object.entries(dados).map(([chave, valor]) => [
        chave,
        Number(valor)
      ])
    )

    try {
      const resposta = await fetch('http://127.0.0.1:8000/simular', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(dadosNumericos)
      })

      if (!resposta.ok) {
        throw new Error('Não foi possível executar a simulação.')
      }

      const resultadoApi = await resposta.json()

      setResultado(resultadoApi)
      setConexao('CONECTADA')

      await carregarHistorico()

    } catch (error) {
      setErro(error.message)
      setConexao('DESCONECTADA')
    } finally {
      setCarregando(false)
    }
  }

  function getStatusClass(status) {
    if (
      status === 'ACIONADO' ||
      status.includes('RISCO') ||
      status.includes('PERIGO') ||
      status.includes('CRITICA')
    ) {
      return 'danger'
    }

    if (status.includes('ATENCAO')) {
      return 'warning'
    }

    return 'success'
  }

  function formatarData(data) {
    return new Date(data).toLocaleString('pt-BR')
  }

  const totalSimulacoes = historico.length

  const totalAeb = historico.filter(
    (simulacao) => simulacao.aeb_acionado
  ).length

  const totalCriticas = historico.filter(
    (simulacao) => simulacao.status_geral.includes('CRITICA')
  ).length

  return (
    <main className="dashboard">

      <header className="header">
        <div>
          <h1>ADAS Simulator</h1>
          <p>Sistema avançado de assistência ao motorista</p>
        </div>

        <span className={`connection ${conexao === 'CONECTADA' ? 'online' : 'offline'}`}>
          API {conexao}
        </span>
      </header>

      <section className="overview">

        <div className="panel">
          <span>VELOCIDADE ATUAL</span>
          <h2>
            {resultado ? `${dados.vel_atual} km/h` : '-- km/h'}
          </h2>

          <div className="speed-track">
            <div
              className="speed-fill"
              style={{
                width: `${Math.min(Number(dados.vel_atual) / 180 * 100, 100)}%`
              }}
            />
          </div>

          <small>Escala de 0 a 180 km/h</small>
        </div>

        <div className="panel">
          <span>DISTÂNCIA SEGURA</span>
          <h2>
            {resultado
              ? `${resultado.distancia_segura.toFixed(2)} m`
              : '-- m'}
          </h2>
        </div>

        <div className="panel">
          <span>STATUS DO SISTEMA</span>
          <h2 className={`status ${resultado ? getStatusClass(resultado.status_geral) : ''}`}>
            {resultado ? resultado.status_geral : 'AGUARDANDO'}
          </h2>
        </div>

      </section>

      {resultado && (
        <div className={`aeb-banner ${getStatusClass(resultado.aeb)}`}>
          <div>
            <strong>SISTEMA DE FRENAGEM AUTOMÁTICA (AEB)</strong>

            <p>
              {resultado.aeb === 'ACIONADO'
                ? 'FRENAGEM DE EMERGÊNCIA ACIONADA'
                : 'SEM NECESSIDADE DE INTERVENÇÃO'}
            </p>
          </div>
        </div>
      )}

      <section className="simulation">
        <h2>Configuração da simulação</h2>
        <p>Informe os dados do veículo e dos sensores.</p>

        <form className="simulation-form" onSubmit={handleSubmit}>

          <div className="form-group">
            <label>Velocidade atual (km/h)</label>
            <input type="number" name="vel_atual" min="0" value={dados.vel_atual} onChange={handleChange} required />
          </div>

          <div className="form-group">
            <label>Velocidade do veículo à frente (km/h)</label>
            <input type="number" name="vel_frente" min="0" value={dados.vel_frente} onChange={handleChange} required />
          </div>

          <div className="form-group">
            <label>Radar (metros)</label>
            <input type="number" name="radar" min="0" step="0.1" value={dados.radar} onChange={handleChange} required />
          </div>

          <div className="form-group">
            <label>LiDAR (metros)</label>
            <input type="number" name="lidar" min="0" step="0.1" value={dados.lidar} onChange={handleChange} required />
          </div>

          <div className="form-group">
            <label>Câmera (metros)</label>
            <input type="number" name="camera" min="0" step="0.1" value={dados.camera} onChange={handleChange} required />
          </div>

          <div className="form-group">
            <label>Atrito da pista</label>
            <input type="number" name="atrito" min="0.01" step="0.01" value={dados.atrito} onChange={handleChange} required />
          </div>

          <div className="form-group">
            <label>Distância da faixa esquerda (metros)</label>
            <input type="number" name="faixa_esq" min="0" step="0.1" value={dados.faixa_esq} onChange={handleChange} required />
          </div>

          <div className="form-group">
            <label>Distância da faixa direita (metros)</label>
            <input type="number" name="faixa_dir" min="0" step="0.1" value={dados.faixa_dir} onChange={handleChange} required />
          </div>

          <div className="form-group">
            <label>Nível de sensibilidade</label>
            <select name="nivel" value={dados.nivel} onChange={handleChange}>
              <option value="1">Baixo</option>
              <option value="2">Médio</option>
              <option value="3">Alto</option>
            </select>
          </div>

          <button type="submit" className="simulate-button" disabled={carregando}>
            {carregando ? 'EXECUTANDO...' : 'EXECUTAR SIMULAÇÃO'}
          </button>

        </form>

        {erro && <p className="error-message">{erro}</p>}

      </section>

      {resultado && (
        <section className="simulation results">
          <h2>Resultados da simulação</h2>

          <div className="result-grid">

            <div>
              <span>Distância validada</span>
              <strong>{resultado.distancia_validada.toFixed(2)} m</strong>
            </div>

            <div>
              <span>Distância segura</span>
              <strong>{resultado.distancia_segura.toFixed(2)} m</strong>
            </div>

            <div>
              <span>Status frontal</span>
              <strong className={getStatusClass(resultado.status_frontal)}>
                {resultado.status_frontal}
              </strong>
            </div>

            <div>
              <span>Sistema AEB</span>
              <strong className={getStatusClass(resultado.aeb)}>
                {resultado.aeb}
              </strong>
            </div>

            <div>
              <span>Faixa esquerda</span>
              <strong className={getStatusClass(resultado.faixa_esquerda)}>
                {resultado.faixa_esquerda}
              </strong>
            </div>

            <div>
              <span>Faixa direita</span>
              <strong className={getStatusClass(resultado.faixa_direita)}>
                {resultado.faixa_direita}
              </strong>
            </div>

            <div>
              <span>Margem lateral</span>
              <strong>{resultado.margem_lateral.toFixed(2)} m</strong>
            </div>

          </div>

          <div className="road-section">
            <h2>Monitoramento de faixas</h2>

            <div className="road">

              <div className="lane-side left">
                <span className={getStatusClass(resultado.faixa_esquerda)} />
              </div>

              <div className="lane-line"></div>

              <div className="car">🚘</div>

              <div className="lane-side right">
                <span className={getStatusClass(resultado.faixa_direita)} />
              </div>

            </div>
          </div>

        </section>
      )}

      <section className="simulation history-section">
        <div className="history-header">
          <div>
            <h2>Histórico de simulações</h2>
            <p>Registros armazenados no PostgreSQL.</p>
          </div>

          <button
            className="history-refresh"
            onClick={carregarHistorico}
            disabled={carregandoHistorico}
          >
            {carregandoHistorico ? 'ATUALIZANDO...' : 'ATUALIZAR'}
          </button>
        </div>

        <div className="history-overview">

          <div className="history-stat">
            <span>TOTAL DE SIMULAÇÕES</span>
            <strong>{totalSimulacoes}</strong>
          </div>

          <div className="history-stat">
            <span>AEB ACIONADO</span>
            <strong className="danger">{totalAeb}</strong>
          </div>

          <div className="history-stat">
            <span>STATUS CRÍTICO</span>
            <strong className="danger">{totalCriticas}</strong>
          </div>

        </div>

        {carregandoHistorico && (
          <p className="history-message">Carregando histórico...</p>
        )}

        {erroHistorico && (
          <p className="error-message">{erroHistorico}</p>
        )}

        {!carregandoHistorico && !erroHistorico && historico.length === 0 && (
          <p className="history-message">
            Nenhuma simulação registrada até o momento.
          </p>
        )}

        {!carregandoHistorico && historico.length > 0 && (
          <div className="history-list">

            {historico.map((simulacao) => (
              <div className="history-card" key={simulacao.id}>

                <div className="history-card-header">
                  <strong>SIMULAÇÃO #{simulacao.id}</strong>
                  <span>{formatarData(simulacao.criado_em)}</span>
                </div>

                <div className="history-details">

                  <div>
                    <span>Velocidade atual</span>
                    <strong>{simulacao.vel_atual} km/h</strong>
                  </div>

                  <div>
                    <span>Distância validada</span>
                    <strong>{simulacao.distancia_validada.toFixed(2)} m</strong>
                  </div>

                  <div>
                    <span>Distância segura</span>
                    <strong>{simulacao.distancia_segura.toFixed(2)} m</strong>
                  </div>

                  <div>
                    <span>Sistema AEB</span>
                    <strong className={simulacao.aeb_acionado ? 'danger' : 'success'}>
                      {simulacao.aeb_acionado ? 'ACIONADO' : 'NÃO ACIONADO'}
                    </strong>
                  </div>

                </div>

                
<button
  type="button"
  className="history-expand"
  onClick={() => alternarDetalhes(simulacao.id)}
  aria-expanded={simulacoesExpandidas.includes(simulacao.id)}
>
  {simulacoesExpandidas.includes(simulacao.id)
    ? 'RECOLHER DETALHES'
    : 'VER DETALHES DA SIMULAÇÃO'}

  <span>
    {simulacoesExpandidas.includes(simulacao.id) ? '▲' : '▼'}
  </span>
</button>

{simulacoesExpandidas.includes(simulacao.id) && (
  <div className="history-expanded">

    <div className="history-detail-group">
      <h3>Dados de entrada</h3>

      <div className="history-data-grid">
        <div>
          <span>Velocidade atual</span>
          <strong>{simulacao.vel_atual} km/h</strong>
        </div>

        <div>
          <span>Velocidade à frente</span>
          <strong>{simulacao.vel_frente} km/h</strong>
        </div>

        <div>
          <span>Radar</span>
          <strong>{simulacao.radar} m</strong>
        </div>

        <div>
          <span>LiDAR</span>
          <strong>{simulacao.lidar} m</strong>
        </div>

        <div>
          <span>Câmera</span>
          <strong>{simulacao.camera} m</strong>
        </div>

        <div>
          <span>Atrito da pista</span>
          <strong>{simulacao.atrito}</strong>
        </div>

        <div>
          <span>Nível de sensibilidade</span>
          <strong>
            {simulacao.nivel === 1
              ? 'Baixo'
              : simulacao.nivel === 2
                ? 'Médio'
                : 'Alto'}
          </strong>
        </div>

        <div>
          <span>Faixa esquerda (entrada)</span>
          <strong>{simulacao.faixa_esq} m</strong>
        </div>

        <div>
          <span>Faixa direita (entrada)</span>
          <strong>{simulacao.faixa_dir} m</strong>
        </div>
      </div>
    </div>

    <div className="history-detail-group">
      <h3>Resultados e decisões do sistema</h3>

      <div className="history-data-grid">
        <div>
          <span>Distância validada</span>
          <strong>{simulacao.distancia_validada.toFixed(2)} m</strong>
        </div>

        <div>
          <span>Distância segura</span>
          <strong>{simulacao.distancia_segura.toFixed(2)} m</strong>
        </div>

        <div>
          <span>Margem lateral</span>
          <strong>{simulacao.margem_lateral.toFixed(2)} m</strong>
        </div>

        <div>
          <span>Status frontal</span>
          <strong className={getStatusClass(simulacao.status_frontal)}>
            {simulacao.status_frontal}
          </strong>
        </div>

        <div>
          <span>Sistema AEB</span>
          <strong className={simulacao.aeb_acionado ? 'danger' : 'success'}>
            {simulacao.aeb_acionado ? 'ACIONADO' : 'NÃO ACIONADO'}
          </strong>
        </div>

        <div>
          <span>Faixa esquerda</span>
          <strong className={getStatusClass(simulacao.faixa_esquerda)}>
            {simulacao.faixa_esquerda}
          </strong>
        </div>

        <div>
          <span>Faixa direita</span>
          <strong className={getStatusClass(simulacao.faixa_direita)}>
            {simulacao.faixa_direita}
          </strong>
        </div>

        <div>
          <span>Status geral</span>
          <strong className={getStatusClass(simulacao.status_geral)}>
            {simulacao.status_geral}
          </strong>
        </div>
      </div>
    </div>

  </div>
)}


                <div className="history-status">
                  <span>STATUS GERAL</span>
                  <strong className={getStatusClass(simulacao.status_geral)}>
                    {simulacao.status_geral}
                  </strong>
                </div>

              </div>
            ))}

          </div>
        )}

      </section>

    </main>
  )
}

export default App