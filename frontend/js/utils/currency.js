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
 * Example: 80000 => Rp. 80.000,00
 * @param {*} costInMinimalUnit Cost in minimal unit (rupiah).
 * @returns Display cost string that may be used in the UI.
 */
export function toDisplayCost(costInMinimalUnit) {
    return `Rp. ${costInMinimalUnit.toLocaleString('id-ID', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}
