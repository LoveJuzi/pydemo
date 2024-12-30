package utils

func ConvInt64(n interface{}) (int64, bool) {
	switch v := n.(type) {
	case int:
		return int64(v), true
	case int64:
		return v, true
	default:
		return 0, false
	}
}

func ConvFloat64(n interface{}) (float64, bool) {
	switch v := n.(type) {
	case int:
		return float64(v), true
	case int64:
		return float64(v), true
	case float32:
		return float64(v), true
	case float64:
		return v, true
	default:
		return 0.0, false
	}
}
