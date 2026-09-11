import { useState } from 'react';

const initialForm = {
  Auction: 'ADESA',
  VehYear: 2018,
  VehicleAge: 3,
  Make: 'FORD',
  Model: 'FUSION',
  Transmission: 'AUTO',
  WheelType: 'Alloy',
  VehOdo: 85000,
  Nationality: 'AMERICAN',
  Size: 'MEDIUM',
  TopThreeAmericanName: 'OTHER',
  Color: 'RED',
  MMRAcquisitionAuctionAveragePrice: 12000,
  MMRAcquisitionAuctionCleanPrice: 14000,
  MMRAcquisitionRetailAveragePrice: 17000,
  MMRAcquisitonRetailCleanPrice: 18600,
  MMRCurrentAuctionAveragePrice: 11000,
  MMRCurrentAuctionCleanPrice: 13000,
  MMRCurrentRetailAveragePrice: 16000,
  MMRCurrentRetailCleanPrice: 17400,
  PRIMEUNIT: 'NULL',
  AUCGUART: 'NULL',
  VNST: 'FL',
  VehBCost: 32000,
  IsOnlineSale: 0,
  WarrantyCost: 1200,
};

function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState({
    status: 'idle',
    message: 'Aguardando análise...',
    confidence: null,
    probabilityBad: null,
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({
      ...prev,
      [name]:
        ['VehYear', 'VehicleAge', 'VehOdo', 'VehBCost', 'WarrantyCost', 'IsOnlineSale'].includes(name)
          ? Number(value)
          : value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setResult({ status: 'idle', message: 'Analisando veículo...', confidence: null, probabilityBad: null });

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        throw new Error('API indisponível em http://localhost:8000');
      }

      const data = await response.json();
      const isRisk = data.prediction === 1;

      setResult({
        status: isRisk ? 'risk' : 'good',
        message: isRisk ? 'Compra de risco' : 'Boa oportunidade',
        confidence: data.confidence,
        probabilityBad: data.probability_bad_buy * 100,
      });
    } catch (error) {
      setResult({
        status: 'error',
        message: 'Erro na análise',
        confidence: null,
        probabilityBad: null,
        detail: 'Verifique se a API está iniciada em http://localhost:8000.',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-shell">
      <div className="container">
        <header className="header">
          <div>
            <p className="eyebrow">CarGuard AI</p>
            <h1>Sistema Inteligente de Avaliação de Veículos Usados</h1>
          </div>
        </header>

        <form onSubmit={handleSubmit} className="form-grid">
          <label>
            Marca
            <input name="Make" value={form.Make} onChange={handleChange} />
          </label>
          <label>
            Modelo
            <input name="Model" value={form.Model} onChange={handleChange} />
          </label>
          <label>
            Ano
            <input type="number" name="VehYear" value={form.VehYear} onChange={handleChange} />
          </label>
          <label>
            Idade do veículo
            <input type="number" name="VehicleAge" value={form.VehicleAge} onChange={handleChange} />
          </label>
          <label>
            Leilão
            <input name="Auction" value={form.Auction} onChange={handleChange} />
          </label>
          <label>
            Transmissão
            <select name="Transmission" value={form.Transmission} onChange={handleChange}>
              <option value="AUTO">AUTO</option>
              <option value="MANUAL">MANUAL</option>
            </select>
          </label>
          <label>
            Cor
            <input name="Color" value={form.Color} onChange={handleChange} />
          </label>
          <label>
            Quilometragem
            <input type="number" name="VehOdo" value={form.VehOdo} onChange={handleChange} />
          </label>
          <label>
            Preço de compra
            <input type="number" name="VehBCost" value={form.VehBCost} onChange={handleChange} />
          </label>
          <label>
            Garantia
            <input type="number" name="WarrantyCost" value={form.WarrantyCost} onChange={handleChange} />
          </label>
          <label>
            Estado
            <input name="VNST" value={form.VNST} onChange={handleChange} />
          </label>
          <label>
            Tamanho
            <select name="Size" value={form.Size} onChange={handleChange}>
              <option value="MEDIUM">MEDIUM</option>
              <option value="COMPACT">COMPACT</option>
              <option value="SUV">SUV</option>
              <option value="LARGE">LARGE</option>
            </select>
          </label>
          <label>
            Venda online
            <select name="IsOnlineSale" value={form.IsOnlineSale} onChange={handleChange}>
              <option value={0}>Não</option>
              <option value={1}>Sim</option>
            </select>
          </label>

          <button type="submit" disabled={loading}>
            {loading ? 'Analisando...' : 'Analisar veículo'}
          </button>
        </form>

        <section className={`result ${result.status}`}>
          <div className="result-title">{result.message}</div>
          {result.confidence !== null && (
            <>
              <p>Confiança do modelo: {result.confidence}%</p>
              <p>Probabilidade de má compra: {Number(result.probabilityBad).toFixed(2)}%</p>
            </>
          )}
          {result.detail && <p className="detail">{result.detail}</p>}
        </section>
      </div>
    </div>
  );
}

export default App;
