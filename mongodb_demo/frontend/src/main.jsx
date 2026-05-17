import React, { useCallback, useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const emptyFilters = {
  productType: "",
  manufacturer: "",
  category: "",
  status: "",
  minPrice: "",
  maxPrice: "",
  ramMin: "",
  shippingRegion: "",
  tag: "",
  schemaEvolution: "",
  search: "",
};

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || payload.error || `Request failed: ${response.status}`);
  }
  return payload;
}

function buildQueryParams(filters) {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (String(value).trim()) {
      params.set(key, String(value).trim());
    }
  });
  return params;
}

function formatCurrency(value, currency) {
  return new Intl.NumberFormat("de-DE", { style: "currency", currency: currency || "EUR" }).format(value || 0);
}

function shortDate(value) {
  if (!value) {
    return "unknown";
  }
  return new Intl.DateTimeFormat("de-DE", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

function formatCell(value) {
  if (typeof value === "number") {
    return Number.isInteger(value) ? String(value) : value.toFixed(2);
  }
  return value ?? "";
}

function App() {
  const [facets, setFacets] = useState(null);
  const [filters, setFilters] = useState(emptyFilters);
  const [products, setProducts] = useState([]);
  const [total, setTotal] = useState(0);
  const [limit, setLimit] = useState(25);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [detailQueryText, setDetailQueryText] = useState("");
  const [detailCodeText, setDetailCodeText] = useState("");
  const [listQueryText, setListQueryText] = useState("");
  const [listCodeText, setListCodeText] = useState("");
  const [activeTab, setActiveTab] = useState("document");
  const [aggregationKind, setAggregationKind] = useState("avgPriceByType");
  const [aggregation, setAggregation] = useState(null);
  const [health, setHealth] = useState({ state: "checking", label: "checking" });
  const [statusMessage, setStatusMessage] = useState("");
  const [sampleType, setSampleType] = useState("laptop");

  const loadHealth = useCallback(async () => {
    try {
      const data = await fetchJson("/api/health");
      setHealth({ state: "ok", label: `${data.productCount} products` });
    } catch (error) {
      setHealth({ state: "error", label: "MongoDB offline" });
      setStatusMessage(error.message);
    }
  }, []);

  const loadFacets = useCallback(async () => {
    const data = await fetchJson("/api/facets");
    setFacets(data);
  }, []);

  const loadProducts = useCallback(async (nextFilters, options = {}) => {
    setStatusMessage("Loading products");
    const params = buildQueryParams(nextFilters);
    const url = params.toString() ? `/api/products?${params}` : "/api/products";
    const data = await fetchJson(url);
    setProducts(data.items);
    setTotal(data.total);
    setLimit(data.limit);
    setListQueryText(data.queryText);
    setListCodeText(data.codeText);
    if (options.clearSelection !== false) {
      setSelectedProduct(null);
      setDetailQueryText("");
      setDetailCodeText("");
    }
    setStatusMessage(data.total ? "" : "No products match the active filters");
  }, []);

  const loadAggregation = useCallback(async (kind) => {
    const data = await fetchJson(`/api/aggregation?kind=${encodeURIComponent(kind)}`);
    setAggregation(data);
  }, []);

  useEffect(() => {
    loadHealth().catch((error) => setStatusMessage(error.message));
    loadFacets().catch((error) => setStatusMessage(error.message));
  }, [loadFacets, loadHealth]);

  useEffect(() => {
    loadAggregation(aggregationKind).catch((error) => setStatusMessage(error.message));
  }, [aggregationKind, loadAggregation]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      loadProducts(filters).catch((error) => setStatusMessage(error.message));
    }, 160);
    return () => window.clearTimeout(timer);
  }, [filters, loadProducts]);

  const selectProduct = async (productId) => {
    setStatusMessage("Loading document");
    const data = await fetchJson(`/api/products/${encodeURIComponent(productId)}`);
    setSelectedProduct(data.item);
    setDetailQueryText(data.queryText);
    setDetailCodeText(data.codeText);
    setStatusMessage("");
  };

  const insertSample = async () => {
    setStatusMessage("Inserting sample product");
    const data = await fetchJson("/api/products/sample", {
      method: "POST",
      body: JSON.stringify({ productType: sampleType }),
    });
    await loadFacets();
    await loadProducts(filters, { clearSelection: false });
    await selectProduct(data.item._id);
    await loadAggregation(aggregationKind);
    await loadHealth();
    setStatusMessage(data.message);
  };

  const updateFilter = (name, value) => {
    setFilters((current) => ({ ...current, [name]: value }));
  };

  const detailText = useMemo(() => {
    if (!selectedProduct) {
      if (activeTab === "query") {
        return listQueryText || "Loading query.";
      }
      if (activeTab === "code") {
        return listCodeText || "Loading code.";
      }
      return "Select a product to inspect its document.";
    }
    if (activeTab === "query") {
      return detailQueryText;
    }
    if (activeTab === "code") {
      return detailCodeText;
    }
    return JSON.stringify(selectedProduct, null, 2);
  }, [activeTab, detailCodeText, detailQueryText, listCodeText, listQueryText, selectedProduct]);

  const aggregationKeys = useMemo(() => {
    if (!aggregation?.results?.length) {
      return [];
    }
    return Array.from(new Set(aggregation.results.flatMap((row) => Object.keys(row))));
  }, [aggregation]);

  const hasTaxCode = selectedProduct && Object.hasOwn(selectedProduct, "regionalTaxCode");

  return (
    <>
      <header className="topbar">
        <div>
          <p className="eyebrow">MongoDB Demo</p>
          <h1>Product Catalog</h1>
        </div>
        <div className="topbar-actions">
          <span className={`status-pill ${health.state}`}>{health.label}</span>
          <select aria-label="Sample product type" value={sampleType} onChange={(event) => setSampleType(event.target.value)}>
            <option value="laptop">Laptop sample</option>
            <option value="t-shirt">T-Shirt sample</option>
            <option value="book">Book sample</option>
            <option value="smartphone">Smartphone sample</option>
            <option value="desk">Desk sample</option>
          </select>
          <button className="primary-button" type="button" onClick={() => insertSample().catch((error) => setStatusMessage(error.message))}>
            Insert Sample
          </button>
        </div>
      </header>

      <main className="workspace">
        <aside className="filter-panel" aria-label="Filters">
          <div className="panel-heading">
            <h2>Filters</h2>
            <button className="ghost-button" type="button" onClick={() => setFilters(emptyFilters)}>
              Reset
            </button>
          </div>
          <form className="filter-grid" onSubmit={(event) => event.preventDefault()}>
            <SelectField label="Type" value={filters.productType} onChange={(value) => updateFilter("productType", value)} options={facets?.productTypes || []} />
            <SelectField label="Manufacturer" value={filters.manufacturer} onChange={(value) => updateFilter("manufacturer", value)} options={facets?.manufacturers || []} />
            <SelectField label="Category" value={filters.category} onChange={(value) => updateFilter("category", value)} options={facets?.categories || []} valueKey="slug" labelKey="name" />
            <SelectField label="Status" value={filters.status} onChange={(value) => updateFilter("status", value)} options={facets?.statuses || []} />
            <InputField label="Min price" type="number" value={filters.minPrice} onChange={(value) => updateFilter("minPrice", value)} placeholder="0" />
            <InputField label="Max price" type="number" value={filters.maxPrice} onChange={(value) => updateFilter("maxPrice", value)} placeholder="2500" />
            <SelectField label="RAM from" value={filters.ramMin} onChange={(value) => updateFilter("ramMin", value)} options={facets?.ramOptions || []} formatLabel={(value) => `${value} GB`} />
            <SelectField label="Ship to" value={filters.shippingRegion} onChange={(value) => updateFilter("shippingRegion", value)} options={facets?.shippingRegions || []} />
            <SelectField label="Tag" value={filters.tag} onChange={(value) => updateFilter("tag", value)} options={facets?.tags || []} />
            <SelectField
              label="Schema"
              value={filters.schemaEvolution}
              onChange={(value) => updateFilter("schemaEvolution", value)}
              options={facets?.schemaEvolution || []}
              valueKey="value"
              labelKey="label"
            />
            <InputField label="Search" type="search" value={filters.search} onChange={(value) => updateFilter("search", value)} placeholder="name or highlight" wide />
          </form>
          <p className="status-message" role="status">
            {statusMessage}
          </p>
        </aside>

        <section className="product-panel" aria-label="Products">
          <div className="panel-heading">
            <h2>Products</h2>
            <span className="muted">
              {total} result{total === 1 ? "" : "s"} / limit {limit}
            </span>
          </div>
          <div className="product-list">
            {products.length ? (
              products.map((product) => (
                <button
                  key={product._id}
                  type="button"
                  className={`product-item ${selectedProduct?._id === product._id ? "active" : ""}`}
                  onClick={() => selectProduct(product._id).catch((error) => setStatusMessage(error.message))}
                >
                  <div>
                    <div className="product-name">{product.name}</div>
                    <div className="product-meta">
                      {formatCurrency(product.basePrice, product.currency)} - {product.manufacturer?.name || "unknown"}
                    </div>
                    <div className="product-category">
                      {product.categories?.[0]?.name || "Uncategorized"} - updated {shortDate(product.updatedAt)}
                    </div>
                  </div>
                  <span className="type-badge">{product.productType}</span>
                </button>
              ))
            ) : (
              <div className="muted empty-state">No matching products.</div>
            )}
          </div>
        </section>

        <section className="detail-panel" aria-label="Product detail">
          <div className="panel-heading">
            <h2>{selectedProduct?.name || "Document"}</h2>
            <div className="tabs" role="tablist" aria-label="Detail views">
              {["document", "query", "code"].map((tab) => (
                <button key={tab} className={`tab-button ${activeTab === tab ? "active" : ""}`} type="button" onClick={() => setActiveTab(tab)}>
                  {tab === "code" ? "PyMongo" : tab[0].toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>
          </div>
          <div className={`schema-hint ${selectedProduct ? (hasTaxCode ? "newer" : "older") : ""}`}>
            {selectedProduct
              ? hasTaxCode
                ? `Schema version ${selectedProduct.schemaVersion}: regionalTaxCode = ${selectedProduct.regionalTaxCode}`
                : `Schema version ${selectedProduct.schemaVersion}: no regionalTaxCode field`
              : "List query is shown until a product is selected."}
          </div>
          <pre className="code-block">{detailText}</pre>
        </section>

        <section className="aggregation-panel" aria-label="Aggregation">
          <div className="panel-heading">
            <h2>Aggregation</h2>
            <select aria-label="Aggregation kind" value={aggregationKind} onChange={(event) => setAggregationKind(event.target.value)}>
              {(facets?.aggregations || []).map((item) => (
                <option key={item.kind} value={item.kind}>
                  {item.label}
                </option>
              ))}
            </select>
          </div>
          <div className="aggregation-layout">
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    {aggregationKeys.map((key) => (
                      <th key={key}>{key === "_id" ? "group" : key}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {(aggregation?.results || []).map((row, index) => (
                    <tr key={`${row._id}-${index}`}>
                      {aggregationKeys.map((key) => (
                        <td key={key}>{formatCell(row[key])}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <pre className="code-block small">{aggregation?.queryText || "Loading aggregation."}</pre>
          </div>
        </section>
      </main>
    </>
  );
}

function SelectField({ label, value, onChange, options, valueKey, labelKey, formatLabel }) {
  return (
    <label>
      {label}
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        <option value="">All</option>
        {options.map((option) => {
          const optionValue = valueKey ? option[valueKey] : option;
          const optionLabel = labelKey ? option[labelKey] : formatLabel ? formatLabel(option) : option;
          return (
            <option key={optionValue} value={optionValue}>
              {optionLabel}
            </option>
          );
        })}
      </select>
    </label>
  );
}

function InputField({ label, type, value, onChange, placeholder, wide = false }) {
  return (
    <label className={wide ? "wide-field" : ""}>
      {label}
      <input
        type={type}
        value={value}
        min={type === "number" ? "0" : undefined}
        step={type === "number" ? "10" : undefined}
        placeholder={placeholder}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  );
}

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
