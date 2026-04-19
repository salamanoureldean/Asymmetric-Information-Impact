#ifndef SOCIAL_CELL_HPP_
#define SOCIAL_CELL_HPP_

#include <cadmium/modeling/celldevs/asymm/cell.hpp>
#include "socialState.hpp"

using namespace cadmium::celldevs;

class socialCell : public AsymmCell<socialState, double> {
public:
    socialCell(
        const std::string& id,
        const std::shared_ptr<const AsymmCellConfig<socialState, double>>& config
    ) : AsymmCell<socialState, double>(id, config) {}

    [[nodiscard]] socialState localComputation(
        socialState state,
        const std::unordered_map<std::string, NeighborData<socialState, double>>& neighborhood
    ) const override {
        double weightedInfluence = 0.0;

        for (const auto& [neighborId, neighborData] : neighborhood) {
            if (neighborData.state == nullptr) continue;

            int nVal = neighborData.state->value;

            if (nVal == 1 || nVal == 2) {
                weightedInfluence += neighborData.vicinity;
            }
        }

        if (state.value == 0 && weightedInfluence >= 0.75) return socialState(1);


        if (state.value == 1 && weightedInfluence >= 2.0) return socialState(2);

        return state;
    }

    [[nodiscard]] double outputDelay(const socialState& state) const override {
        return 100.0;
    }
};

#endif