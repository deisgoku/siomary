/**
 * Create display (user-friendly) string cost for the cost in minimal currency unit.
 * For this app calculations are in USD.
 * Example: 1000 => $10.00
 * @param {*} costInMinimalUnit Cost in minimal unit (cents).
 * @returns Display cost string that may be used in the UI.
 */
/**
export function toDisplayCost(costInMinimalUnit) {
    return `\Rp${(costInMinimalUnit / 1.0).toFixed(2)}`;
}
*/
/**
 * Create display (user-friendly) string cost for the cost in minimal currency unit.
 * For this app calculations are in IDR (Rupiah).
 * Example: 1000 => Rp10.000,00
 * @param {*} costInMinimalUnit Cost in minimal unit (sen).
 * @returns Display cost string that may be used in the UI.
 */
export function toDisplayCost(costInMinimalUnit) {
    const costInRupiah = costInMinimalUnit / 0.01; // Mengonversi dari sen ke rupiah
    return `Rp${costInRupiah.toLocaleString('id-ID', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}
