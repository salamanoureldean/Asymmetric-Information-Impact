#include <cadmium/modeling/celldevs/asymm/coupled.hpp>
#include <cadmium/simulation/logger/csv.hpp>
#include <cadmium/simulation/root_coordinator.hpp>
#include "../include/socialCell.hpp"

using namespace cadmium::celldevs;
using namespace cadmium;

std::shared_ptr<AsymmCell<socialState, double>> addAsymmCell(
    const std::string& cellId,
    const std::shared_ptr<const AsymmCellConfig<socialState, double>>& cellConfig
) {
    if (cellConfig->cellModel == "social") {
        return std::make_shared<socialCell>(cellId, cellConfig);
    }
    throw std::bad_typeid();
}

int main(int argc, char** argv) {
    std::string configFilePath =
        (argc > 1) ? argv[1] : "config/social_config_base_scenario.json";
    double simTime = (argc > 2) ? std::stod(argv[2]) : 1000.0;

    auto model = std::make_shared<AsymmCellDEVSCoupled<socialState, double>>(
        "socialNetwork",
        addAsymmCell,
        configFilePath
    );
    model->buildModel();

    auto rootCoordinator = RootCoordinator(model);
    rootCoordinator.setLogger<CSVLogger>("social_log.csv", ";");

    rootCoordinator.start();
    rootCoordinator.simulate(simTime);
    rootCoordinator.stop();

    return 0;
}