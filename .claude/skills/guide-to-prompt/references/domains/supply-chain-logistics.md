# Supply Chain & Logistics

**Axis 0 domain.** Canonical label, do not rename it. Every task sits in exactly one domain, and the one to pick is the one whose decision-maker would actually own the call.

- **Typical decisions:** Inventory, sourcing, routing, fulfillment decisions
- **Typical data:** Shipment, inventory, carrier, and procurement records

## Enumerated subdomains

Pick one and write it into `DATASET_NOTES.md` with the domain. These lists are a browsing aid rather than a closed set, but a subdomain you cannot map to one of these is a signal to change the trap, not to stretch the scope.

- **Inventory & demand planning:** demand and shipment forecasting, replenishment, safety stock; stockouts, fill rate; lead-time variability
- **Sourcing & procurement flow:** supplier selection, single vs dual-sourcing, allocation; landed cost and supplier scorecards
- **Transportation & network:** routing, carrier on-time performance; distribution-network and lane design
- **Trade & flows:** imports and exports by commodity, exposure and concentration; port and border performance
- **Fulfillment & warehousing:** pick/pack productivity, dock-to-stock, distribution-center performance
- **Other:** anything else about the movement, flow, or handling of physical goods

## Example prompts

The worked example prompts live in `../shapes/`, filed by prompt shape. Read them as idea
seeds for what a task in this domain can be about. **Never copy one into a build**: not the
scenario, not the entity, not the metric,
not a file name, not the wording of an ask. The anti-clone draw in
`../../../stumping/SKILL.md` Part 6 is what turns a seed into a fresh build.
