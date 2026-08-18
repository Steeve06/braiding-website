export function formatDuration(totalMinutes) {
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;

  if (hours === 0) {
    return `${minutes} min`;
  }
  if (minutes === 0) {
    return `${hours} hr`;
  }
  return `${hours} hr ${minutes} min`;
}

export function formatPrice(rawPrice) {
  const numericPrice = Number(rawPrice);
  return `$${numericPrice.toFixed(0)}`;
}

export function formatCategoryLabel(rawCategory) {
  return rawCategory.replace(/_/g, " ");
}
