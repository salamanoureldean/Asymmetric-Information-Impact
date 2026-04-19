#ifndef SOCIAL_STATE_HPP_
#define SOCIAL_STATE_HPP_

#include <nlohmann/json.hpp>
#include <iostream>

struct socialState {
    int value;

    explicit socialState(int v = 0) : value(v) {}
};

inline bool operator==(const socialState& x, const socialState& y) {
    return x.value == y.value;
}

inline bool operator!=(const socialState& x, const socialState& y) {
    return !(x == y);
}

inline std::ostream& operator<<(std::ostream& out, const socialState& s) {
    out << "<" << s.value << ">";
    return out;
}

inline void from_json(const nlohmann::json& j, socialState& s) {
    j.at("value").get_to(s.value);
}

#endif